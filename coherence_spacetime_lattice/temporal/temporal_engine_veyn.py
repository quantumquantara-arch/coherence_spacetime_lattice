"""
temporal_engine_veyn.py

Temporal channels are treated as histories of κ–τ–Σ plus derived invariants.
This makes the module empirical: channels can be compared quantitatively.

Key invariants:
  - responsibility score S = (⟨κ⟩⟨τ⟩)/(1+⟨Σ⟩)
  - coherence retention: slope of ⟨κ⟩ over time (linear fit)
  - separation growth: slope of ⟨Σ⟩ over time (linear fit)

The engine ranks channels by a composite score (defaults can be adjusted).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Optional

import numpy as np

from src.coherence_field import CoherenceMetrics


def _linear_slope(y: np.ndarray) -> float:
    if y.size < 2:
        return 0.0
    x = np.arange(y.size, dtype=float)
    x = x - np.mean(x)
    y = y - np.mean(y)
    denom = float(np.dot(x, x))
    if denom <= 0.0:
        return 0.0
    return float(np.dot(x, y) / denom)


@dataclass
class TemporalChannel:
    name: str
    sequence: List[CoherenceMetrics] = field(default_factory=list)

    def add(self, metrics: CoherenceMetrics) -> None:
        self.sequence.append(metrics)

    def _arr(self) -> np.ndarray:
        if not self.sequence:
            return np.zeros((0, 3), dtype=float)
        return np.array([[m.kappa, m.tau, m.sigma] for m in self.sequence], dtype=float)

    def averages(self) -> CoherenceMetrics:
        a = self._arr()
        if a.size == 0:
            return CoherenceMetrics(0.0, 0.0, 0.0)
        return CoherenceMetrics(float(np.mean(a[:, 0])), float(np.mean(a[:, 1])), float(np.mean(a[:, 2])))

    def average_kappa(self) -> float:
        return self.averages().kappa

    def average_tau(self) -> float:
        return self.averages().tau

    def average_sigma(self) -> float:
        return self.averages().sigma

    def temporal_responsibility_score(self) -> float:
        a = self.averages()
        return (a.kappa * a.tau) / (1.0 + a.sigma)

    def coherence_retention_slope(self) -> float:
        a = self._arr()
        return _linear_slope(a[:, 0]) if a.size else 0.0

    def separation_growth_slope(self) -> float:
        a = self._arr()
        return _linear_slope(a[:, 2]) if a.size else 0.0


@dataclass(frozen=True)
class RankingWeights:
    w_resp: float = 1.0
    w_kappa_slope: float = 0.5
    w_sigma_slope: float = 0.5  # penalized


class TemporalEngineVeyn:
    def __init__(self, *, weights: Optional[RankingWeights] = None):
        self.channels: List[TemporalChannel] = []
        self.weights = weights or RankingWeights()

    def add_channel(self, channel: TemporalChannel) -> None:
        self.channels.append(channel)

    def channel_score(self, ch: TemporalChannel) -> float:
        w = self.weights
        resp = ch.temporal_responsibility_score()
        ksl = ch.coherence_retention_slope()
        ssl = ch.separation_growth_slope()
        return w.w_resp * resp + w.w_kappa_slope * ksl - w.w_sigma_slope * ssl

    def rank_channels_by_responsibility(self) -> List[TemporalChannel]:
        return sorted(self.channels, key=self.channel_score, reverse=True)

    def ranked_table(self) -> List[Tuple[str, float, float, float, float]]:
        """
        Returns (name, score, resp, kappa_slope, sigma_slope) rows.
        """
        out: List[Tuple[str, float, float, float, float]] = []
        for ch in self.rank_channels_by_responsibility():
            out.append(
                (
                    ch.name,
                    self.channel_score(ch),
                    ch.temporal_responsibility_score(),
                    ch.coherence_retention_slope(),
                    ch.separation_growth_slope(),
                )
            )
        return out
