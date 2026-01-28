import matplotlib.pyplot as plt

def plot_tour(
    cities,
    tour,
    title="TSP Tour",
    show_index=False,
    save_path=None,
    show=True
):
    xs = cities[:, 0]
    ys = cities[:, 1]

    # close the loop
    tour_cycle = tour + [tour[0]]
    tour_x = xs[tour_cycle]
    tour_y = ys[tour_cycle]

    plt.figure()
    plt.plot(tour_x, tour_y, "-o")
    plt.title(title)

    if show_index:
        for i, (x, y) in enumerate(cities):
            plt.text(x, y, str(i))

    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=150)

    if show:
        plt.show()
    else:
        plt.close()
