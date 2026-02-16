import numpy as np
import matplotlib.pyplot as plt

from spacetime.spacetime_lattice import SpacetimeLattice


def main():
    lattice = SpacetimeLattice(120, 120, dx=1.0, alpha_metric=0.6)
    lattice.initialize_center_pulse()

    steps = 250
    for _ in range(steps):
        lattice.step(dt=0.08)

    snap = lattice.snapshot()

    fig, axs = plt.subplots(2, 3, figsize=(12, 8))
    axs = axs.ravel()

    for ax, key in zip(
        axs,
        ["kappa", "tau", "sigma", "phi", "metric_scale", "curvature_proxy"],
    ):
        im = ax.imshow(snap[key], origin="lower")
        ax.set_title(key)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.show()

    # plot aggregate metrics
    k = [m.kappa for m in lattice.history]
    t = [m.tau for m in lattice.history]
    s = [m.sigma for m in lattice.history]

    plt.figure(figsize=(8, 4))
    plt.plot(k, label="avg κ")
    plt.plot(t, label="avg τ")
    plt.plot(s, label="avg Σ")
    plt.legend()
    plt.xlabel("step")
    plt.title("Aggregate κ–τ–Σ history")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
