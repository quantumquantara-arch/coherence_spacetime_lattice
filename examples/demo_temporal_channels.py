"""
demo_temporal_channels.py

Example demonstrating how to compare temporal channels using the Veyn engine.

Workflow:
- run the same initial lattice under different update rules,
- record κ–τ–Σ histories,
- load them into TemporalChannel objects,
- compare temporal responsibility scores.
"""

from coherence_spacetime_lattice import (
    SpacetimeLattice,
    TemporalEngineVeyn,
    TemporalChannel,
)


def run_policy(name, steps, local_update=None):
    lattice = SpacetimeLattice(height=15, width=15)
    lattice.initialize_center_pulse()
    lattice.run(steps=steps, local_update=local_update)
    channel = TemporalChannel(name=name)
    for metrics in lattice.history:
        channel.add(metrics)
    return channel


if __name__ == "__main__":
    steps = 40

    # Policy A: default local dynamics.
    channel_a = run_policy("policy_default", steps=steps)

    # Policy B: more aggressive τ reinforcement (example).
    def aggressive_tau(field):
        field.step_local_dynamics(alpha_kappa=0.2, beta_sigma=0.1, gamma_tau=0.2)

    channel_b = run_policy("policy_aggressive_tau", steps=steps, local_update=aggressive_tau)

    engine = TemporalEngineVeyn()
    engine.add_channel(channel_a)
    engine.add_channel(channel_b)

    ranked = engine.rank_channels_by_responsibility()
    print("Channels ranked by temporal responsibility score:")
    for ch in ranked:
        print(
            f"{ch.name}: "
            f"score={ch.temporal_responsibility_score():.4f}, "
            f"avg κ={ch.average_kappa():.4f}, "
            f"avg τ={ch.average_tau():.4f}, "
            f"avg Σ={ch.average_sigma():.4f}"
        )
