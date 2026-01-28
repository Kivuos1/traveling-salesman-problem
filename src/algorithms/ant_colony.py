import random
import numpy as np
from tsp.tour import tour_length


def ant_colony_optimization(
    dist,
    *,
    n_ants=30,
    n_iters=200,
    alpha=1.0,
    beta=5.0,
    rho=0.5,
    q=1.0,
    seed=None,
    closed=True,
    start_city=None,
    return_history=False,
):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    n = len(dist)
    if n < 2:
        if return_history:
            return [0], 0.0, [0.0]
        return [0], 0.0

    eps = 1e-12
    eta = 1.0 / (dist + eps)
    np.fill_diagonal(eta, 0.0)

    tau0 = 1.0
    tau = np.full((n, n), tau0, dtype=float)
    np.fill_diagonal(tau, 0.0)

    best_tour = None
    best_len = float("inf")
    history = []

    def pick_next(current, unvisited):
        unv = list(unvisited)
        weights = []
        for j in unv:
            w = (tau[current, j] ** alpha) * (eta[current, j] ** beta)
            weights.append(w)

        total = sum(weights)
        if total <= 0.0:
            return random.choice(unv)

        r = random.random() * total
        cum = 0.0
        for j, w in zip(unv, weights):
            cum += w
            if cum >= r:
                return j
        return unv[-1]

    for _ in range(n_iters):
        all_tours = []
        all_lens = []

        for _ant in range(n_ants):
            start = random.randrange(n) if start_city is None else start_city

            tour = [start]
            unvisited = set(range(n))
            unvisited.remove(start)

            current = start
            while unvisited:
                nxt = pick_next(current, unvisited)
                tour.append(nxt)
                unvisited.remove(nxt)
                current = nxt

            L = tour_length(tour, dist, closed=closed)
            all_tours.append(tour)
            all_lens.append(L)

            if L < best_len:
                best_len = L
                best_tour = tour[:]

        history.append(best_len)

        tau *= (1.0 - rho)

        idx_best = int(np.argmin(all_lens))
        it_best_tour = all_tours[idx_best]
        it_best_len = all_lens[idx_best]
        deposit = q / it_best_len

        for i in range(n - 1):
            a = it_best_tour[i]
            b = it_best_tour[i + 1]
            tau[a, b] += deposit
            tau[b, a] += deposit

        if closed:
            a = it_best_tour[-1]
            b = it_best_tour[0]
            tau[a, b] += deposit
            tau[b, a] += deposit

        np.fill_diagonal(tau, 0.0)

    if return_history:
        return best_tour, best_len, history
    return best_tour, best_len
