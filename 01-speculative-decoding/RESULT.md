# Result: Speculative Decoding — Is It Actually a Free Speedup?

## The claim being tested

Speculative decoding is widely described as a straightforward win for LLM
inference speed: pair a big model with a small, cheap "draft" model, let
the draft model guess several tokens ahead, and have the big model verify
them all in a single pass instead of generating one token at a time. The
implicit assumption in most explanations is that this is close to a free
upgrade — add a draft model, get a faster system.

This experiment checks whether that holds regardless of how good the draft
model is, or whether the benefit depends on draft accuracy in a way that
can also work against you.

## Method

A simplified simulation stands in for the real mechanism, since the goal
was to isolate the algorithm's behavior rather than model real neural
network performance:

- A "big model" step costs 50ms; a "draft model" step costs 5ms.
- The draft model proposes 4 tokens ahead per round with a fixed accuracy
  (a coin-flip against that accuracy determines whether each guess is
  correct).
- The big model verifies the drafted tokens in one pass; the run accepts
  every correct guess and stops at the first wrong one, where the big
  model supplies the correct token itself.
- Total time is compared against normal, one-token-at-a-time generation
  for a 200-token sequence, across draft accuracies from 90% down to 10%.

## Result

| Draft accuracy | Speedup |
|---|---|
| 90% | 2.34x |
| 70% | 1.70x |
| 50% | 1.26x |
| 30% | 0.97x |
| 10% | 0.80x |

The relationship isn't linear speedup falls off sharply as accuracy
drops, and it crosses the 1.0x break-even point right around 30% draft
accuracy. Below that, speculative decoding is measurably *slower* than
just running the big model normally.

## Why this happens

The draft model isn't free just because it's cheap. Every guess it makes
still costs time, and every wrong guess is a guess you paid for and threw
away. When the draft model is right most of the time, the big model
mostly gets to skip ahead. When it's wrong most of the time, you're
paying the draft model's cost on top of the big model's cost, with almost
nothing to show for it. The 30% mark isn't a rule, just where these
particular costs and this lookahead setting happen to balance out — but
the shape of the curve is the real point: there's a real cost to running
a bad draft model, not just a missed opportunity.

## Limitations

- This is a simulation, not a test with real neural networks. Real draft
  models don't have a single, constant accuracy they tend to do better
  on predictable, common continuations and worse on unusual ones, so
  real-world speedup would vary within a single generation rather than
  stay fixed like it does here.
- The 5ms/50ms cost ratio and the break-even point are specific to the
  parameters chosen in this run. Changing the draft model's relative cost
  or the lookahead length would shift where the break-even point sits
  worth testing as a follow-up rather than assuming this threshold is
  universal.

## Takeaway

Speculative decoding's speedup isn't guaranteed just by adding a draft
model it depends on the draft model actually being good enough at
predicting what the big model would say. Below some threshold, it can
make generation slower, not faster. That's a meaningfully different claim
than "speculative decoding speeds things up," and it's the kind of detail
that doesn't show up until you actually run the numbers instead of taking
the pitch at face value.
