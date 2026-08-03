"""
Day 2 — Continuous Batching vs. Static Batching

THE IDEA:
When an LLM server handles multiple requests at once, it groups them into a
"batch" that runs together on the GPU. The question is how that batch is
managed as individual requests finish at different times (since a request
asking for 20 tokens finishes way before one asking for 200).

STATIC BATCHING: a fixed group of N requests runs together, and the WHOLE
BATCH is stuck running until the slowest request in it finishes. Every slot
whose request finished early just sits idle, burning GPU time for nothing,
until the last request in the batch is done. Only then can a new batch start.

CONTINUOUS BATCHING: the moment any single request finishes, a new request
from the queue immediately takes its slot — no waiting for the whole batch.

THE CLAIM BEING TESTED:
Continuous batching is described as a clear improvement over static
batching. This experiment checks HOW MUCH better it is, and specifically
whether the gap depends on how much request lengths vary. If all requests
need roughly the same number of tokens, static batching shouldn't waste much
— the real question is what happens once lengths become uneven, which is
the realistic case for real chat/completion traffic.

METRIC: GPU utilization = useful tokens actually generated / total GPU
"slot-steps" consumed (a slot-step = one GPU slot busy for one token-step,
whether or not that slot is doing useful work).
"""

import random
from collections import deque

random.seed(42)

BATCH_SIZE = 8
NUM_REQUESTS = 200


def generate_request_lengths(n, mean, spread):
    """
    Generate n request lengths (number of tokens each request needs).
    `spread` controls variability: 0 = all requests identical length,
    higher = more uneven mix of short and long requests.
    """
    lengths = []
    for _ in range(n):
        length = max(1, int(random.gauss(mean, spread)))
        lengths.append(length)
    return lengths


def simulate_static_batching(lengths, batch_size):
    """
    Process requests in fixed-size batches. A batch can't start the next
    one until every request in the current batch has finished — so the
    batch's duration is set by its SLOWEST request, and every faster
    request's leftover slot-steps are wasted (idle).
    """
    total_steps = 0
    total_slot_steps = 0

    for i in range(0, len(lengths), batch_size):
        batch = lengths[i:i + batch_size]
        batch_duration = max(batch)              # slowest request sets the pace
        total_steps += batch_duration
        total_slot_steps += len(batch) * batch_duration  # every slot busy the whole time, even if idle

    return total_steps, total_slot_steps


def simulate_continuous_batching(lengths, batch_size):
    """
    The moment any active slot's request finishes, immediately refill it
    from the queue. No slot waits on the batch's slowest member — it only
    goes idle if there's nothing left in the queue to give it.
    """
    queue = deque(lengths)
    active = []  # list of remaining-token-counts for requests currently running

    while queue and len(active) < batch_size:
        active.append(queue.popleft())

    total_steps = 0
    total_slot_steps = 0

    while active:
        total_steps += 1
        total_slot_steps += len(active)

        still_active = []
        for remaining in active:
            remaining -= 1
            if remaining > 0:
                still_active.append(remaining)
        active = still_active

        while queue and len(active) < batch_size:
            active.append(queue.popleft())

    return total_steps, total_slot_steps


def main():
    mean_length = 30
    spreads_to_test = [0, 5, 10, 20, 40]

    print(f"{'spread':>7} | {'static steps':>13} | {'cont steps':>11} | {'static util':>12} | {'cont util':>10} | {'speedup':>8}")
    print("-" * 75)

    for spread in spreads_to_test:
        lengths = generate_request_lengths(NUM_REQUESTS, mean_length, spread)
        total_tokens = sum(lengths)

        static_steps, static_slot_steps = simulate_static_batching(lengths, BATCH_SIZE)
        cont_steps, cont_slot_steps = simulate_continuous_batching(lengths, BATCH_SIZE)

        static_util = total_tokens / static_slot_steps
        cont_util = total_tokens / cont_slot_steps
        speedup = static_steps / cont_steps

        print(f"{spread:>7} | {static_steps:>13} | {cont_steps:>11} | {static_util:>11.1%} | {cont_util:>9.1%} | {speedup:>7.2f}x")


if __name__ == "__main__":
    main()