def nearest_neighbor(dist, start=0):
    """
    Nearest Neighbor heuristic for TSP.
    """
    n = len(dist)
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)

    current = start
    while unvisited:
        next_city = min(unvisited, key=lambda c: dist[current][c])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return tour
