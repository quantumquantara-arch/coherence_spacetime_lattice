"""
coherence_field.py

Defines:
- CoherenceMetrics: small dataclass for κ, τ, Σ at a point.
- CoherenceField: 2D lattice storing coherence values and simple evolution rules.

A simple reference implementation — extensible for larger or more serious physics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional

import numpy as np


@dataclass
class CoherenceMetrics:
    """
    κ–τ–Σ metrics at a single lattice point.

    κ (kappa): coherence density
    τ (tau): temporal responsibility
    Σ (sigma): systemic separation / hidden entropy
    """
    kappa: float
    tau: float
    sigma: float

    def as_array(self) -> np.ndarray:
        return np.array([self.kappa, self.tau, self.sigma], dtype=float)


class CoherenceField:
    """
    2D coherence field on a rectangular lattice.

    Internally: field[h, w, :] = (κ, τ, Σ)

    Provides:
    - initialization (random, pulse, uniform)
    - local-update dynamics (toy coherence evolution)
    - aggregate metric computation
    """

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.field = np.zeros((height, width, 3), dtype=float)

    def initialize_center_pulse(
        self,
        kappa_peak: float = 1.0,
        radius: int = 3,
        tau_value: float = 0.5,
        sigma_value: float = 0.1,
    ) -> None:
        """
        Seed a coherent pulse at the center of the lattice.
        """
        cy, cx = self.height // 2, self.width // 2
        for y in range(self.height):
            for x in range(self.width):
                dy = y - cy
                dx = x - cx
                if dy * dy + dx * dx <= radius * radius:
                    self.field[y, x, 0] = kappa_peak
                    self.field[y, x, 1] = tau_value
                    self.field[y, x, 2] = sigma_value

    def randomize(
        self,
        kappa_range: Tuple[float, float] = (0.0, 1.0),
        tau_range: Tuple[float, float] = (0.0, 1.0),
        sigma_range: Tuple[float, float] = (0.0, 1.0),
        seed: Optional[int] = None,
    ) -> None:
        """
        Random initialization for κ, τ, Σ.
        """
        rng = np.random.default_rng(seed)
        self.field[:, :, 0] = rng.uniform(*kappa_range, size=(self.height, self.width))
        self.field[:, :, 1] = rng.uniform(*tau_range, size=(self.height, self.width))
        self.field[:, :, 2] = rng.uniform(*sigma_range, size=(self.height, self.width))

    def get_metrics(self, y: int, x: int) -> CoherenceMetrics:
        """
        Retrieve κ–τ–Σ at (y, x).
        """
        kappa, tau, sigma = self.field[y, x, :]
        return CoherenceMetrics(float(kappa), float(tau), float(sigma))

    def set_metrics(self, y: int, x: int, metrics: CoherenceMetrics) -> None:
        """
        Set κ–τ–Σ at (y, x).
        """
        self.field[y, x, :] = metrics.as_array()

    def neighborhood_average(self, y: int, x: int) -> CoherenceMetrics:
        """
        Average κ–τ–Σ over the local 3×3 patch around (y, x).
        """
        ys = max(0, y - 1)
        ye = min(self.height, y + 2)
        xs = max(0, x - 1)
        xe = min(self.width, x + 2)

        patch = self.field[ys:ye, xs:xe, :]
        avg = np.mean(patch, axis=(0, 1))
        return CoherenceMetrics(kappa=float(avg[0]), tau=float(avg[1]), sigma=float(avg[2]))

    def step_local_dynamics(
        self,
        alpha_kappa: float = 0.2,
        beta_sigma: float = 0.1,
        gamma_tau: float = 0.1,
    ) -> None:
        """
        One update of local coherence dynamics.

        Rules (toy model):
        - κ diffuses toward neighbors.
        - Σ decreases when τ and κ are high (responsible suppression of separation).
        - τ increases when κ is high and Σ is low (ethical reinforcement).
        """
        new_field = self.field.copy()

        for y in range(self.height):
            for x in range(self.width):
                local = self.get_metrics(y, x)
                neigh = self.neighborhood_average(y, x)

                # κ diffuses toward neighborhood.
                k_new = local.kappa + alpha_kappa * (neigh.kappa - local.kappa)

                # Σ is suppressed by τ and κ.
                sigma_reduction = beta_sigma * local.tau * local.kappa
                s_new = max(0.0, local.sigma - sigma_reduction)

                # τ reinforced when κ high + Σ low.
                tau_increment = gamma_tau * local.kappa * (1.0 - local.sigma)
                t_new = min(1.0, local.tau + tau_increment)

                new_field[y, x, 0] = k_new
                new_field[y, x, 1] = t_new
                new_field[y, x, 2] = s_new

        self.field = new_field

    def aggregate_metrics(self) -> CoherenceMetrics:
        """
        Return average κ–τ–Σ over the entire field.
        """
        avg = np.mean(self.field, axis=(0, 1))
        return CoherenceMetrics(kappa=float(avg[0]), tau=float(avg[1]), sigma=float(avg[2]))
