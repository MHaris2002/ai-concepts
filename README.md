# AI Systems — Mechanism Studies

Small, from-scratch implementations that test whether specific claims
about AI/ML techniques actually hold up under controlled conditions,
rather than taking them at face value.

Each entry: one technique, a minimal simulation or implementation of its
core mechanism, and a measured result.

## Entries

| # | Technique | Question tested | Result |
|---|-----------|-----------------|--------|
| 01 | [Speculative Decoding](01-speculative-decoding/) | Does draft-model accuracy determine whether the technique actually speeds up generation, and where's the break-even point? | Speedup scales with draft accuracy and crosses break-even (1.0x) around 30% accuracy — below that, it's slower than normal decoding. |
| 02 | [Continuous Batching](02-continuous-batching/) | Does static batching waste GPU capacity compared to continuous batching, and does the gap depend on request-length variance? | Static batching utilization drops from 100% to 37.5% as request-length variance increases; continuous batching holds ~100% regardless. |
| 03 | [Self-Consistency](03-self-consistency/) | Does majority-vote sampling across N independent samples actually improve accuracy, and does it depend on how good the model already is? | Voting drives accuracy toward ~100% when base accuracy is ≥0.5, but barely helps when base accuracy is only marginally above chance (0.3 → 0.509 even at N=41). |

## Structure
Each numbered folder contains:
- `experiment.py` — the implementation/simulation
- `RESULT.md` — findings, methodology, and limitations