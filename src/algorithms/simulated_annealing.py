import math
import random
from tsp.tour import tour_length


def two_opt_swap_inplace(tour, i, k):
    tour[i:k+1] = reversed(tour[i:k+1])


def simulated_annealing(
    init_tour,
    dist,
    *,
    start_temp=1.0,
    end_temp=1e-4,
    alpha=0.995,
    iters_per_temp=200,
    seed=None,
    closed=True,
    return_history=False,
):
    if seed is not None:
        random.seed(seed)

    n = len(init_tour)
    current = init_tour[:]
    current_len = tour_length(current, dist, closed=closed)

    best = current[:]
    best_len = current_len

    history = [best_len]

    T = float(start_temp)
    while T > end_temp:
        for _ in range(iters_per_temp):
            i = random.randint(1, n - 2)
            k = random.randint(i + 1, n - 1)

            candidate = current[:]
            two_opt_swap_inplace(candidate, i, k)
            cand_len = tour_length(candidate, dist, closed=closed)

            delta = cand_len - current_len

            if delta < 0 or random.random() < math.exp(-delta / T):
                current = candidate
                current_len = cand_len

                if current_len < best_len:
                    best = current[:]
                    best_len = current_len
                    history.append(best_len)

        T *= alpha

    if return_history:
        return best, best_len, history
    return best, best_len
