import matplotlib.pyplot as plt

def plot_convergence(
    histories,
    labels,
    title="Convergence (best length so far)",
    save_path=None,
    show=True
):
    plt.figure()

    for hist, label in zip(histories, labels):
        if hist:
            plt.plot(hist, label=label)

    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("Best tour length")
    plt.legend()
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=150)

    if show:
        plt.show()
    else:
        plt.close()
