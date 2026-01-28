import time

from tsp.instance import generate_euclidean
from tsp.distance import distance_matrix
from tsp.tour import tour_length
from algorithms.nearest_neighbor import nearest_neighbor
from algorithms.two_opt import two_opt
from algorithms.simulated_annealing import simulated_annealing
from viz.plot_tour import plot_tour
from algorithms.genetic import genetic_algorithm
from algorithms.ant_colony import ant_colony_optimization
from viz.plot_convergence import plot_convergence


def timed(label, fn):
    t0 = time.perf_counter()
    out = fn()
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(f"{label} time: {elapsed:.6f} s")
    return out, elapsed


def main():
    n = 30
    cities = generate_euclidean(n, seed=42)
    dist = distance_matrix(cities)
    algo_seeds = [0, 1, 2]
    results = []

    # --- Nearest Neighbor (baseline) ---
    t0 = time.perf_counter()
    nn_tour = nearest_neighbor(dist, start=0)
    nn_time = time.perf_counter() - t0

    nn_len = tour_length(nn_tour, dist)
    print(f"Nearest Neighbor tour length: {nn_len:.4f}  time={nn_time:.6f}s")

    # --- 2-opt local search ---
    t0 = time.perf_counter()
    opt_tour, opt_len = two_opt(nn_tour, dist)
    opt_time = time.perf_counter() - t0

    print(f"2-opt improved tour length: {opt_len:.4f}  time={opt_time:.6f}s")
    print(f"Improvement over NN: {(nn_len - opt_len):.4f}")


    for s in algo_seeds:
        print(f"\n--- Run with algorithm seed = {s} ---")

        # --- Simulated Annealing ---
        t0 = time.perf_counter()
        sa_tour, sa_len, sa_hist = simulated_annealing(
            opt_tour, dist,
            start_temp=0.5, end_temp=1e-4,
            alpha=0.995, iters_per_temp=300,
            seed=s, return_history=True
        )
        sa_time = time.perf_counter() - t0
        print(f"SA:  len={sa_len:.4f}, time={sa_time:.4f}s")

        # --- Genetic Algorithm ---
        t0 = time.perf_counter()
        ga_tour, ga_len, ga_hist = genetic_algorithm(
            dist,
            pop_size=250, generations=600,
            tournament_k=4,
            crossover_rate=0.9, mutation_rate=0.25,
            elite_size=3,
            seed=s,
            init_tour=sa_tour,
            return_history=True
        )
        ga_time = time.perf_counter() - t0
        print(f"GA:  len={ga_len:.4f}, time={ga_time:.4f}s")

        # --- Ant Colony Optimization ---
        t0 = time.perf_counter()
        aco_tour, aco_len, aco_hist = ant_colony_optimization(
            dist,
            n_ants=30, n_iters=200,
            alpha=1.0, beta=5.0,
            rho=0.5, q=1.0,
            seed=s,
            return_history=True
        )
        aco_time = time.perf_counter() - t0
        print(f"ACO: len={aco_len:.4f}, time={aco_time:.4f}s")

        results.extend([
            ("SA",  s, sa_len,  sa_time),
            ("GA",  s, ga_len,  ga_time),
            ("ACO", s, aco_len, aco_time),
        ])


    with open("data/outputs/results.txt", "w") as f:
        f.write("Algorithm, Seed, TourLength, TimeSeconds\n")
        for algo, seed, length, secs in results:
            f.write(f"{algo}, {seed}, {length:.6f}, {secs:.6f}\n")

    # --- Convergence plot (last seed only) ---
    plot_convergence(
        histories=[sa_hist, ga_hist, aco_hist],
        labels=["Simulated Annealing", "Genetic Algorithm", "Ant Colony"],
        title="TSP Metaheuristics Convergence",
        save_path="data/outputs/convergence.png",
        show=False
    )

    # --- Time & Quality Summary (last seed only) ---
    print("\n=== Time & Quality Summary (last seed) ===")
    rows = [
        ("Nearest Neighbor", nn_len, nn_time),
        ("2-opt", opt_len, opt_time),
        ("Simulated Annealing", sa_len, sa_time),
        ("Genetic Algorithm", ga_len, ga_time),
        ("Ant Colony", aco_len, aco_time),
    ]

    for name, length, secs in rows:
        print(f"{name:22s}  length={length:8.4f}  time={secs:9.6f} s")

    # --- Tour visualizations (last seed only) ---
    plot_tour(
        cities, nn_tour,
        title=f"Nearest Neighbor (len={nn_len:.3f})",
        save_path="data/outputs/nn_tour.png",
        show=False
    )

    plot_tour(
        cities, opt_tour,
        title=f"2-opt (len={opt_len:.3f})",
        save_path="data/outputs/opt_tour.png",
        show=False
    )

    plot_tour(
        cities, sa_tour,
        title=f"Simulated Annealing (len={sa_len:.3f})",
        save_path="data/outputs/sa_tour.png",
        show=False
    )

    plot_tour(
        cities, ga_tour,
        title=f"Genetic Algorithm (len={ga_len:.3f})",
        save_path="data/outputs/ga_tour.png",
        show=False
    )

    plot_tour(
        cities, aco_tour,
        title=f"Ant Colony Optimization (len={aco_len:.3f})",
        save_path="data/outputs/aco_tour.png",
        show=False
    )


    #print("SA improvement over 2-opt:", round(opt_len - sa_len, 4))
    #print("GA improvement over SA:", round(sa_len - ga_len, 4))
    #print("ACO improvement over SA:", round(sa_len - aco_len, 4))


if __name__ == "__main__":
    main()

