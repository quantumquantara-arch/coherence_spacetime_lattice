"""
spacetime_lattice.py

Defines the SpacetimeLattice, which couples a CoherenceField
to a discrete time-stepping rule.

This is the main "simulation" object for coherence-spacetime experiments.
"""

from __future__ import annotations

from typing import Callable, Optional, List

from .coherence_field import CoherenceField, CoherenceMetrics


class SpacetimeLattice:
    """
    A 2D spacetime lattice carrying a CoherenceField.

    Attributes:
        field: underlying CoherenceField instance.
        history: list of aggregate CoherenceMetrics over time.
        time_step: current discrete time index.
    """

    def __init__(self, height: int, width: int):
        self.field = CoherenceField(height, width)
        self.history: List[CoherenceMetrics] = []
        self.time_step: int = 0

    def initialize_center_pulse(self) -> None:
        """
        Convenience wrapper: seed a central coherence pulse.
        """
        self.field.initialize_center_pulse()

    def step(
        self,
        local_update: Optional[Callable[[CoherenceField], None]] = None,
    ) -> None:
        """
        Advance the lattice by one discrete time step.

        Args:
            local_update: optional function that receives the CoherenceField
                          and mutates it in place. If None, uses the
                          default step_local_dynamics() on the field.
        """
        if local_update is None:
            self.field.step_local_dynamics()
        else:
            local_update(self.field)

        self.time_step += 1
        self.history.append(self.field.aggregate_metrics())

    def run(
        self,
        steps: int,
        local_update: Optional[Callable[[CoherenceField], None]] = None,
    ) -> None:
        """
        Run the lattice for a given number of steps.

        Args:
            steps: number of discrete updates to perform.
            local_update: optional custom update function
                          (same semantics as in step()).
        """
        for _ in range(steps):
            self.step(local_update=local_update)
