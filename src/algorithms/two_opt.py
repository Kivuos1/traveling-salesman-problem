from tsp.tour import tour_length

def two_opt_swap(tour, i, k):
    """
    Return a new tour where the segment tour[i:k+1] is reversed.
    """
    new_tour = tour[:i] + list(reversed(tour[i:k+1])) + tour[k+1:]
    return new_tour

def two_opt(tour, dist, closed=True):
    """
    Classic 2-opt local search.
    Repeatedly applies improving 2-opt swaps until no improvement remains.

    tour: list of city indices (initial tour)
    dist: distance matrix
    closed: whether to treat the tour as a cycle (TSP)
    """
    best = tour[:]
    best_len = tour_length(best, dist, closed=closed)

    improved = True
    n = len(best)

    while improved:
        improved = False

        # i and k are the segment boundaries we reverse
        # For a closed tour, skipping i=0 with k=n-1 can avoid trivial full reversal;
        # but it's not required. We'll just avoid reversing the entire tour.
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                if i == 0 and k == n - 1:
                    continue

                candidate = two_opt_swap(best, i, k)
                cand_len = tour_length(candidate, dist, closed=closed)

                if cand_len < best_len:
                    best = candidate
                    best_len = cand_len
                    improved = True
                    break  # restart search from scratch (first-improvement)
            if improved:
                break

    return best, best_len
