"""
Plots speedup vs. draft-model accuracy from experiment.py's logic,
including the break-even line at 1.0x, so the finding is visible at a
glance instead of buried in a table.

Requires matplotlib: pip install matplotlib
"""

import matplotlib.pyplot as plt
from experiment import normal_decoding, speculative_decoding, SEQUENCE_LENGTH

DRAFT_STEP_MS = 5
LOOKAHEAD = 4
ACCURACIES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]

baseline_ms, _ = normal_decoding(SEQUENCE_LENGTH)

speedups = []
for acc in ACCURACIES:
    elapsed_ms, _, _ = speculative_decoding(SEQUENCE_LENGTH, acc, LOOKAHEAD, DRAFT_STEP_MS)
    speedups.append(baseline_ms / elapsed_ms)

plt.figure(figsize=(8, 5))
plt.plot(ACCURACIES, speedups, marker="o", label="Speculative decoding speedup")
plt.axhline(y=1.0, color="red", linestyle="--", label="Break-even (1.0x)")
plt.xlabel("Draft model accuracy")
plt.ylabel("Speedup vs. normal decoding")
plt.title("Speculative Decoding: Speedup vs. Draft Model Accuracy")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("speedup_vs_accuracy.png", dpi=150)
print("Saved chart to speedup_vs_accuracy.png")