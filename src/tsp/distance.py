import numpy as np

def distance_matrix(cities):
    """
    Compute Euclidean distance matrix for city coordinates.
    """
    n = len(cities)
    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist[i, j] = np.linalg.norm(cities[i] - cities[j])

    return dist
