# AI Systems - Mechanism Studies

Small, from-scratch implementations that test whether specific claims
about AI/ML techniques actually hold up under controlled conditions,
rather than taking them at face value.

Each entry: one technique, a minimal simulation or implementation of its
core mechanism, and a measured result.

## Entries

| # | Technique | Question tested | Result |
|---|-----------|-----------------|--------|
| 01 | Speculative Decoding | Does draft-model accuracy determine whether the technique actually speeds up generation, and where's the break-even point? | TBD |

## Structure
Each numbered folder contains:
- `experiment.py` - the implementation/simulation
- `RESULT.md` - findings, methodology, and limitations