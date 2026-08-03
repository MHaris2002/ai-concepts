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

## Structure
Each numbered folder contains:
- `experiment.py` — the implementation/simulation
- `RESULT.md` — findings, methodology, and limitations