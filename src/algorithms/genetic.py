import random
from tsp.tour import tour_length


def random_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def tournament_select(population, fitnesses, k=3):
    n = len(population)
    best_idx = None
    for _ in range(k):
        idx = random.randrange(n)
        if best_idx is None or fitnesses[idx] < fitnesses[best_idx]:
            best_idx = idx
    return population[best_idx]


def order_crossover(parent1, parent2):
    n = len(parent1)
    a = random.randint(0, n - 2)
    b = random.randint(a + 1, n - 1)

    child = [None] * n
    child[a:b + 1] = parent1[a:b + 1]
    used = set(child[a:b + 1])

    p2_idx = 0
    for i in range(n):
        if child[i] is not None:
            continue
        while parent2[p2_idx] in used:
            p2_idx += 1
        child[i] = parent2[p2_idx]
        used.add(child[i])
        p2_idx += 1

    return child


def mutate_swap(tour, mutation_rate=0.2):
    if random.random() < mutation_rate:
        n = len(tour)
        i = random.randrange(n)
        j = random.randrange(n)
        tour[i], tour[j] = tour[j], tour[i]


def genetic_algorithm(
    dist,
    *,
    pop_size=200,
    generations=500,
    tournament_k=3,
    crossover_rate=0.9,
    mutation_rate=0.2,
    elite_size=2,
    seed=None,
    closed=True,
    init_tour=None,
    return_history=False,
):
    if seed is not None:
        random.seed(seed)

    n = len(dist)
    if n < 2:
        if return_history:
            return [0], 0.0, [0.0]
        return [0], 0.0

    population = []
    if init_tour is not None:
        population.append(init_tour[:])

    while len(population) < pop_size:
        population.append(random_tour(n))

    def eval_pop(pop):
        return [tour_length(t, dist, closed=closed) for t in pop]

    fitnesses = eval_pop(population)

    best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
    best = population[best_idx][:]
    best_len = fitnesses[best_idx]

    history = [best_len]

    for _ in range(generations):
        ranked = sorted(zip(population, fitnesses), key=lambda x: x[1])
        new_population = [tour[:] for tour, _ in ranked[:elite_size]]

        while len(new_population) < pop_size:
            p1 = tournament_select(population, fitnesses, k=tournament_k)
            p2 = tournament_select(population, fitnesses, k=tournament_k)

            if random.random() < crossover_rate:
                child = order_crossover(p1, p2)
            else:
                child = p1[:]

            mutate_swap(child, mutation_rate=mutation_rate)
            new_population.append(child)

        population = new_population
        fitnesses = eval_pop(population)

        gen_best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
        gen_best_len = fitnesses[gen_best_idx]

        if gen_best_len < best_len:
            best_len = gen_best_len
            best = population[gen_best_idx][:]

        # record best-so-far EVERY generation (so the line is visible)
        history.append(best_len)


    if return_history:
        return best, best_len, history
    return best, best_len
