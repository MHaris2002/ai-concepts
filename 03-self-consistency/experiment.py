"""
Day 3 — Self-Consistency: Does Voting Across More Samples Actually Help?

THE IDEA:
"Test-time compute" is one of the biggest trends in AI right now — instead
of a model answering in one pass, let it spend extra compute at inference
time to think harder, without changing any model weights. One of the
simplest versions of this is SELF-CONSISTENCY: ask the model the same
question N times independently, then take a majority vote over the N
answers instead of trusting any single one.

THE CLAIM BEING TESTED:
Self-consistency is often described as a reliable way to buy accuracy with
compute — sample more, get a better answer. This experiment checks:
  1. Does majority voting actually improve accuracy as N grows?
  2. Are there diminishing returns — does it eventually flatten out?
  3. Does it depend on how good the model already is at the task (its
     single-sample accuracy)? Specifically: can voting rescue a model that's
     wrong more often than it's right?

METHOD:
Simulate a multiple-choice task with `num_options` choices. A single model
sample gets the correct answer with probability `base_accuracy`; when
wrong, it picks uniformly among the remaining wrong options (a reasonable
stand-in for "confidently wrong in different ways each time," which is
what real sampling with temperature > 0 tends to look like). For each
combination of base accuracy and N, run many independent trials and
measure how often the MAJORITY vote across N samples is correct.
"""

import random
from collections import Counter

random.seed(42)

NUM_OPTIONS = 4
TRIALS_PER_CONFIG = 5000
N_VALUES = [1, 3, 5, 9, 15, 25, 41]
BASE_ACCURACIES = [0.3, 0.4, 0.5, 0.6, 0.7]

CORRECT_ANSWER = "A"
WRONG_OPTIONS = ["B", "C", "D"][:NUM_OPTIONS - 1]


def draw_sample(base_accuracy):
    """One independent model sample: correct with probability base_accuracy,
    otherwise a uniformly random wrong option."""
    if random.random() < base_accuracy:
        return CORRECT_ANSWER
    return random.choice(WRONG_OPTIONS)


def majority_vote(samples):
    """Return the most common answer; ties broken randomly."""
    counts = Counter(samples)
    top_count = max(counts.values())
    winners = [option for option, count in counts.items() if count == top_count]
    return random.choice(winners)


def run_trial(base_accuracy, n):
    samples = [draw_sample(base_accuracy) for _ in range(n)]
    return majority_vote(samples) == CORRECT_ANSWER


def main():
    print(f"{'base acc':>9} | " + " | ".join(f"N={n:<3}" for n in N_VALUES))
    print("-" * (11 + 9 * len(N_VALUES)))

    results = {}
    for base_acc in BASE_ACCURACIES:
        row = []
        for n in N_VALUES:
            correct_count = sum(run_trial(base_acc, n) for _ in range(TRIALS_PER_CONFIG))
            accuracy = correct_count / TRIALS_PER_CONFIG
            row.append(accuracy)
        results[base_acc] = row
        print(f"{base_acc:>9.1f} | " + " | ".join(f"{a:.3f}" for a in row))

    return results


if __name__ == "__main__":
    main()