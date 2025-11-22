"""
demo_lattice_evolution.py

Minimal example: create a spacetime lattice,
seed a central coherent pulse, and let it evolve.
"""

from coherence_spacetime_lattice import SpacetimeLattice

if __name__ == "__main__":
    lattice = SpacetimeLattice(height=25, width=25)
    lattice.initialize_center_pulse()

    steps = 50
    for _ in range(steps):
        lattice.step()

    final = lattice.history[-1]
    print("Final aggregate metrics:")
    print(f"κ (coherence): {final.kappa:.4f}")
    print(f"τ (temporal responsibility): {final.tau:.4f}")
    print(f"Σ (systemic separation): {final.sigma:.4f}")
