# Result: Continuous Batching — How Much Does Request-Length Variance Actually Cost You?

## The claim being tested

Continuous batching is described as an improvement over static batching
for serving multiple LLM requests at once. The pitch is straightforward:
instead of waiting for an entire batch of requests to finish before
starting the next batch, slot new requests in the moment any one finishes.
This experiment checks how large that advantage actually is, and
specifically whether it depends on how much request lengths vary — since
if every request needed the same number of tokens, there'd be nothing to
gain from switching strategies at all.

## Method

200 simulated requests, each needing some number of output tokens drawn
from a normal distribution centered at 30 tokens. Five different levels of
"spread" (variance) were tested, from 0 (every request identical length)
up to 40 (a wide mix of short and long requests) — batch size fixed at 8
concurrent slots throughout.

Two scheduling strategies were simulated:

- **Static batching:** requests are grouped into fixed batches of 8. A
  batch can't move on to new requests until every request in it has
  finished, so the batch's total duration is set by its slowest member.
  Any slot whose request finished early sits idle for the rest of that
  batch.
- **Continuous batching:** the moment any slot's request finishes, the
  next request in the queue immediately takes that slot. No slot waits on
  the batch's slowest member.

The main metric is GPU utilization: the fraction of total slot-time that
was spent doing useful work (generating tokens) versus sitting idle.

## Result

| Length variance (spread) | Static utilization | Continuous utilization | Speedup |
|---|---|---|---|
| 0 (all identical) | 100.0% | 100.0% | 1.00x |
| 5 | 78.6% | 100.0% | 1.25x |
| 10 | 67.7% | 100.0% | 1.42x |
| 20 | 49.8% | 100.0% | 1.94x |
| 40 | 37.5% | 100.0% | 2.46x |

Continuous batching holds essentially perfect utilization regardless of
variance. Static batching degrades sharply as request lengths become more
uneven — by the highest variance level tested, nearly two-thirds of its
GPU time is wasted sitting idle.

## Why this happens

Static batching's problem isn't really about batching — it's about being
forced to wait for the slowest request in a group before anyone can move
on. When all requests happen to need about the same number of tokens
(spread = 0), there's no "slowest" member to wait for in any meaningful
sense, so static batching loses nothing. The moment lengths become mixed —
which is the normal case for real traffic, since a one-word reply and a
long explanation both hit the same server — every short request's slot
sits idle for however much longer the batch's longest request still has
to run. Continuous batching sidesteps this entirely by never tying one
request's completion to another's.

## Limitations

- This simulation assumes all 200 requests are available upfront and
  queued instantly, rather than arriving over time the way real traffic
  does. Real-world results would also depend on arrival rate relative to
  service rate, not just length variance.
- Request lengths here are drawn from a single distribution shape (normal,
  clipped at a minimum of 1). Real request-length distributions are often
  more skewed (many short requests, a long tail of very long ones), which
  could make the gap even larger — worth testing directly rather than
  assuming.
- Batch size was held fixed at 8. Whether the relative advantage of
  continuous batching changes with batch size is a natural follow-up.

## Takeaway

The benefit of continuous batching isn't a fixed number — it scales
directly with how uneven your request lengths are. For a workload where
every request is roughly the same length, the two strategies are
equivalent. For realistic, mixed-length traffic, static batching can waste
the majority of its GPU capacity on idle slots, which is a concrete,
measurable cost rather than just a theoretical inefficiency.