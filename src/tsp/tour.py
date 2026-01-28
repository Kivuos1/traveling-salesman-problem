def tour_length(tour, dist, closed=True):
    """
    Compute total length of a tour.
    tour: list of city indices
    dist: distance matrix
    closed: return to start if True
    """
    length = 0.0

    for i in range(len(tour) - 1):
        length += dist[tour[i], tour[i + 1]]

    if closed:
        length += dist[tour[-1], tour[0]]

    return length
