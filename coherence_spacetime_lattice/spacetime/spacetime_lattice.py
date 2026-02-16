"""
spacetime_lattice.py

Couples a CoherenceField to time-stepping and adds "emergent geometry" diagnostics.

This is NOT GR. It provides computable proxies that let the repo move beyond concept:
  - coherence potential Φ from κ
  - metric proxy g_ij = (1 + α Φ) δ_ij in 2D (conformal-flat toy)
  - curvature proxy R ~ -∇² log(1 + α Φ) (2D conformal scalar curvature form, up to conventions)

These proxies are intentionally minimal but mathematically well-defined.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Literal, Dict

import numpy as np

from src.coherence_field import CoherenceField, CoherenceMetrics, _laplacian_5pt


MetricMode = Literal["conformal_2d"]


@dataclass(frozen=True)
class GeometryDiagnostics:
    mean_phi: float
    mean_metric_scale: float
    mean_curvature_proxy: float


class SpacetimeLattice:
    def __init__(
        self,
        height: int,
        width: int,
        *,
        dx: float = 1.0,
        metric_mode: MetricMode = "conformal_2d",
        alpha_metric: float = 0.5,
    ):
        self.field = CoherenceField(height, width, dx=dx)
        self.history: List[CoherenceMetrics] = []
        self.geometry_history: List[GeometryDiagnostics] = []
        self.time_step: int = 0

        self.metric_mode = metric_mode
        self.alpha_metric = float(alpha_metric)

    def initialize_center_pulse(self) -> None:
        self.field.initialize_center_pulse()

    def coherence_potential_phi(self) -> np.ndarray:
        """
        Define Φ as a smoothed coherence potential from κ:
          Φ = κ - <κ>  (mean-centered)
        """
        k = self.field.kappa
        return k - float(np.mean(k))

    def metric_scale(self) -> np.ndarray:
        """
        Conformal metric scale factor:
          Ω = 1 + α Φ
        """
        phi = self.coherence_potential_phi()
        Omega = 1.0 + self.alpha_metric * phi
        return np.maximum(Omega, 1e-6)

    def curvature_proxy(self) -> np.ndarray:
        """
        2D conformal curvature proxy:
          R_proxy = - ∇² log(Ω)
        """
        Omega = self.metric_scale()
        logO = np.log(Omega)
        lap = _laplacian_5pt(logO) / (self.field.dx * self.field.dx)
        return -lap

    def geometry_diagnostics(self) -> GeometryDiagnostics:
        phi = self.coherence_potential_phi()
        Omega = self.metric_scale()
        R = self.curvature_proxy()
        return GeometryDiagnostics(
            mean_phi=float(np.mean(phi)),
            mean_metric_scale=float(np.mean(Omega)),
            mean_curvature_proxy=float(np.mean(R)),
        )

    def step(
        self,
        local_update: Optional[Callable[[CoherenceField], None]] = None,
        *,
        dt: Optional[float] = None,
    ) -> None:
        if local_update is None:
            self.field.step_local_dynamics(dt=dt)
        else:
            local_update(self.field)

        self.time_step += 1
        self.history.append(self.field.aggregate_metrics())
        self.geometry_history.append(self.geometry_diagnostics())

    def run(
        self,
        steps: int,
        local_update: Optional[Callable[[CoherenceField], None]] = None,
        *,
        dt: Optional[float] = None,
    ) -> None:
        for _ in range(int(steps)):
            self.step(local_update=local_update, dt=dt)

    def snapshot(self) -> Dict[str, np.ndarray]:
        """
        Convenience for examples: return fields and geometry.
        """
        return {
            "kappa": self.field.kappa.copy(),
            "tau": self.field.tau.copy(),
            "sigma": self.field.sigma.copy(),
            "phi": self.coherence_potential_phi(),
            "metric_scale": self.metric_scale(),
            "curvature_proxy": self.curvature_proxy(),
        }
