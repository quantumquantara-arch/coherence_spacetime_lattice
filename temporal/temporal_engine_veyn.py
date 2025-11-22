Toy implementation of the Veyn-inspired temporal coherence engine.

Key ideas:
- A "temporal channel" is a sequence of κ–τ–Σ metrics over steps.
- τ (temporal responsibility) measures how well a channel preserves
  coherence vs dumping separation (Σ) into the future.
- Channels can be ranked by temporal_responsibility_score().

This module treats time as "phase-locked coherence history."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .coherence_field import CoherenceMetrics


@dataclass
class TemporalChannel:
    """
    A temporal channel: ordered κ–τ–Σ metrics over time.
    """
    name: str
    sequence: List[CoherenceMetrics] = field(default_factory=list)

    def add(self, metrics: CoherenceMetrics) -> None:
        self.sequence.append(metrics)

    def average_kappa(self) -> float:
        if not self.sequence:
            return 0.0
        return sum(m.kappa for m in self.sequence) / len(self.sequence)

    def average_tau(self) -> float:
        if not self.sequence:
            return 0.0
        return sum(m.tau for m in self.sequence) / len(self.sequence)

    def average_sigma(self) -> float:
        if not self.sequence:
            return 0.0
        return sum(m.sigma for m in self.sequence) / len(self.sequence)

    def temporal_responsibility_score(self) -> float:
        """
        Scalar measure of temporal responsibility.

        High κ and τ increase the score; high Σ penalizes it.
        """
        if not self.sequence:
            return 0.0

        avg_k = self.average_kappa()
        avg_t = self.average_tau()
        avg_s = self.average_sigma()

        return (avg_k * avg_t) / (1.0 + avg_s)


class TemporalEngineVeyn:
    """
    Manages and compares multiple temporal channels.

    Usage:
    - simulate multiple policies,
    - load κ–τ–Σ histories into channels,
    - rank channels by temporal responsibility.
    """

    def __init__(self):
        self.channels: List[TemporalChannel] = []

    def add_channel(self, channel: TemporalChannel) -> None:
        self.channels.append(channel)

    def rank_channels_by_responsibility(self) -> List[TemporalChannel]:
        """
        Return channels sorted by temporal responsibility score (descending).
        """
        return sorted(
            self.channels,
            key=lambda ch: ch.temporal_responsibility_score(),
            reverse=True,
        )
