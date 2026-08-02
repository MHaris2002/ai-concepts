import random
random.seed(42)

VOCAB = list("abcdefghijklmnopqrstuvwxyz ")
SEQUENCE_LENGTH = 200
BIG_MODEL_STEP_MS = 50


def true_next_token(context):
    """Stand-in for 'what the big model would generate.'"""
    return VOCAB[len(context) % len(VOCAB)]


def normal_decoding(sequence_length):
    context = ""
    steps = 0
    while len(context) < sequence_length:
        context += true_next_token(context)
        steps += 1
    elapsed_ms = steps * BIG_MODEL_STEP_MS
    return elapsed_ms, steps


def draft_guess(context, accuracy):
    """
    Stand-in for a small draft model's guess. With probability = accuracy,
    it guesses correctly (matches what the big model would pick).
    Otherwise it guesses a plausible-but-wrong token.
    """
    correct = true_next_token(context)
    if random.random() < accuracy:
        return correct
    wrong_options = [t for t in VOCAB if t != correct]
    return random.choice(wrong_options)


def speculative_decoding(sequence_length, draft_accuracy, lookahead, draft_step_ms):
    """
    Simulate: draft model proposes `lookahead` tokens, big model verifies
    all of them in ONE forward pass, accept the matching prefix, repeat.
    """
    context = ""
    big_model_steps = 0
    draft_model_steps = 0

    while len(context) < sequence_length:
        drafted = []
        draft_context = context
        for _ in range(lookahead):
            guess = draft_guess(draft_context, draft_accuracy)
            drafted.append(guess)
            draft_context += guess
        draft_model_steps += lookahead

        big_model_steps += 1
        for guess in drafted:
            correct = true_next_token(context)
            if guess == correct:
                context += guess
            else:
                context += correct
                break

        if len(context) >= sequence_length:
            break

    elapsed_ms = (big_model_steps * BIG_MODEL_STEP_MS) + (draft_model_steps * draft_step_ms)
    return elapsed_ms, big_model_steps, draft_model_steps


if __name__ == "__main__":
    DRAFT_STEP_MS = 5
    LOOKAHEAD = 4
    ACCURACIES_TO_TEST = [0.9, 0.7, 0.5, 0.3, 0.1]

    baseline_ms, baseline_steps = normal_decoding(SEQUENCE_LENGTH)
    print(f"Baseline (no speculation): {baseline_steps} big-model steps, {baseline_ms}ms\n")

    print(f"{'draft acc':>10} | {'big steps':>10} | {'draft steps':>12} | {'total ms':>9} | {'speedup':>8}")
    print("-" * 60)

    for acc in ACCURACIES_TO_TEST:
        elapsed_ms, big_steps, draft_steps = speculative_decoding(
            SEQUENCE_LENGTH, acc, LOOKAHEAD, DRAFT_STEP_MS
        )
        speedup = baseline_ms / elapsed_ms
        print(f"{acc:>10.1f} | {big_steps:>10} | {draft_steps:>12} | {elapsed_ms:>9} | {speedup:>7.2f}x")