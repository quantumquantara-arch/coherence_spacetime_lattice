"""
impossible_devices.py

Mathematically specified toy devices (not engineering designs).

Each device computes measurable indices from κ–τ–Σ fields:
  - CoherenceThruster: thrust-like vector from asymmetry of ∇κ, gated by τ and penalized by Σ.
  - TemporalInductor: smoothing operator strength based on κ–τ–Σ aggregates.

These are useful for simulations and tests because they produce deterministic outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

from src.coherence_field import CoherenceMetrics, CoherenceField


@dataclass
class DeviceState:
    name: str
    internal_kappa: float
    internal_tau: float
    internal_sigma: float


class CoherenceThruster:
    """
    Thrust proxy from field gradients:

      F = C * ⟨ (τ / (1+Σ)) ∇κ ⟩_A

    where ⟨·⟩_A is spatial average and C is a scaling constant (dimensionless here).
    """

    def __init__(self, state: DeviceState, *, scale: float = 1.0):
        self.state = state
        self.scale = float(scale)

    def thrust_index(self) -> float:
        k = self.state.internal_kappa
        t = self.state.internal_tau
        s = self.state.internal_sigma
        return (k * t) / (1.0 + s)

    def thrust_vector_from_field(self, field: CoherenceField) -> Tuple[float, float]:
        k = field.kappa
        t = field.tau
        s = field.sigma

        # gradient (reflecting edges)
        kx = np.diff(np.pad(k, ((0, 0), (0, 1)), mode="edge"), axis=1) / field.dx
        ky = np.diff(np.pad(k, ((0, 1), (0, 0)), mode="edge"), axis=0) / field.dx

        gate = t / (1.0 + s)
        Fx = self.scale * float(np.mean(gate * kx))
        Fy = self.scale * float(np.mean(gate * ky))
        return (Fx, Fy)


class TemporalInductor:
    """
    Smoothing proxy:

      S = capacity * bias * (⟨κ⟩⟨τ⟩)/(1+⟨Σ⟩)

    Used as a scalar strength for temporal filtering in higher-level code.
    """

    def __init__(self, capacity: float, responsibility_bias: float):
        self.capacity = float(capacity)
        self.responsibility_bias = float(responsibility_bias)

    def smoothing_factor(self, metrics: CoherenceMetrics) -> float:
        return (
            self.capacity
            * self.responsibility_bias
            * (metrics.kappa * metrics.tau)
            / (1.0 + metrics.sigma)
        )


def summarize_device_states(devices: Dict[str, DeviceState]) -> Dict[str, float]:
    summary: Dict[str, float] = {}
    for name, st in devices.items():
        summary[name] = (st.internal_kappa * st.internal_tau) / (1.0 + st.internal_sigma)
    return summary
