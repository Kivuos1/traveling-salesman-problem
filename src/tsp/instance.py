import numpy as np

def generate_euclidean(n, seed=None):
    """
    Generate n cities with (x, y) coordinates in [0, 1] x [0, 1].
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.rand(n, 2)
