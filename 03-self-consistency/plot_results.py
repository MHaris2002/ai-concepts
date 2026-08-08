"""
Plots majority-vote accuracy vs. number of samples (N), one line per base
accuracy, so the diminishing-returns / threshold effect is visible at a
glance instead of buried in a table.

Requires matplotlib: pip install matplotlib
"""

import matplotlib.pyplot as plt
from experiment import run_trial, N_VALUES, BASE_ACCURACIES, TRIALS_PER_CONFIG

plt.figure(figsize=(9, 6))

for base_acc in BASE_ACCURACIES:
    accuracies = []
    for n in N_VALUES:
        correct_count = sum(run_trial(base_acc, n) for _ in range(TRIALS_PER_CONFIG))
        accuracies.append(correct_count / TRIALS_PER_CONFIG)
    plt.plot(N_VALUES, accuracies, marker="o", label=f"base accuracy = {base_acc}")

plt.axhline(y=0.25, color="gray", linestyle=":", label="Random guess baseline (0.25)")
plt.xlabel("Number of samples (N)")
plt.ylabel("Majority-vote accuracy")
plt.title("Self-Consistency: Accuracy vs. Sample Count, by Base Accuracy")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("accuracy_vs_samples.png", dpi=150)
print("Saved chart to accuracy_vs_samples.png")