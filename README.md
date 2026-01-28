# Traveling Salesman Problem (TSP)

This project implements and compares classic heuristic and metaheuristic
approaches to the **Travelling Salesman Problem (TSP)** — finding the shortest
possible tour that visits each city exactly once and returns to the start.

The emphasis is on **solution quality vs runtime tradeoffs** rather than exact
solutions, which are infeasible for large instances.

---

## Problem Setup

- Cities: 30 randomly generated points in 2D
- Distance metric: Euclidean
- Same TSP instance used for all algorithms
- Stochastic algorithms evaluated using multiple random seeds

---

## Algorithms Implemented

### Baselines
- **Nearest Neighbor (NN)**  
  Greedy heuristic; extremely fast but produces suboptimal tours.

- **2-opt Local Search**  
  Deterministic improvement over NN by removing crossing edges.

### Metaheuristics
- **Simulated Annealing (SA)**  
  Probabilistic local search that occasionally accepts worse solutions to
  escape local minima.

- **Genetic Algorithm (GA)**  
  Population-based evolutionary approach using tournament selection,
  order crossover, and mutation.

- **Ant Colony Optimization (ACO)**  
  Pheromone-based collective search inspired by ant foraging behavior.

---

## Experimental Methodology

- NN and 2-opt are run once (deterministic for this setup).
- SA, GA, and ACO are each run **3 times** with different random seeds.
- All runs record:
  - final tour length
  - wall-clock runtime
- Visualizations correspond to the final seed run.

---

## Results Summary (example)

| Algorithm | Tour Length | Time (s) |
|---------|------------|----------|
| NN | ~5.62 | ~0.0001 |
| 2-opt | ~4.98 | ~0.018 |
| SA | ~4.52 | ~4.0 |
| GA | ~4.52 | ~2.3 |
| ACO | ~4.54 | ~1.7 |

Full results for all seeds are stored in:

