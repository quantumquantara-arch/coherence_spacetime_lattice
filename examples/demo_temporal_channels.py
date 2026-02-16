from spacetime.spacetime_lattice import SpacetimeLattice
from temporal.temporal_engine_veyn import TemporalEngineVeyn, TemporalChannel, RankingWeights


def run_policy(name: str, *, alpha_metric: float, dt: float, steps: int) -> TemporalChannel:
    lat = SpacetimeLattice(80, 80, alpha_metric=alpha_metric)
    lat.initialize_center_pulse()

    ch = TemporalChannel(name=name)
    for _ in range(steps):
        lat.step(dt=dt)
        ch.add(lat.history[-1])
    return ch


def main():
    engine = TemporalEngineVeyn(weights=RankingWeights(w_resp=1.0, w_kappa_slope=0.7, w_sigma_slope=0.7))

    engine.add_channel(run_policy("stable_dt_small", alpha_metric=0.5, dt=0.06, steps=200))
    engine.add_channel(run_policy("aggressive_dt", alpha_metric=0.5, dt=0.10, steps=200))
    engine.add_channel(run_policy("high_metric_coupling", alpha_metric=0.9, dt=0.06, steps=200))

    for row in engine.ranked_table():
        name, score, resp, ksl, ssl = row
        print(f"{name:22s} score={score: .5f}  resp={resp: .5f}  dκ/dt={ksl: .5f}  dΣ/dt={ssl: .5f}")


if __name__ == "__main__":
    main()
