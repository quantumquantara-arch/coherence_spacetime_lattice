"""
lumeren_tensor.py

Sketch of a Luméren-inspired symbolic–geometric tensor language.

Purpose:
Represent mathematical structures not only as algebraic expressions,
but as tensors with:
- semantic roles,
- geometric meaning,
- explicit coherence relationships,
- and symbolic connectivity.

This is a minimal but extensible first layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class LumerenSymbol:
    """
    A Luméren symbol with semantic role and arity.

    Attributes:
        name: display label, e.g. "κ", "τ", "Σ", "E".
        role: semantic meaning (coherence, time, risk, cycle, etc.).
        arity: expected number of tensor indices.
        metadata: optional dictionary for glyph info or canonical equations.
    """
    name: str
    role: str
    arity: int = 0
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class LumerenTensor:
    """
    Structural tensor composed of:
    - a LumerenSymbol,
    - index labels,
    - connections to other tensors.

    This is not numeric — it is a representation system for
    higher-order symbolic reasoning and equation design.
    """
    symbol: LumerenSymbol
    indices: List[str] = field(default_factory=list)
    connections: List["LumerenTensor"] = field(default_factory=list)

    def add_connection(self, other: "LumerenTensor") -> None:
        self.connections.append(other)

    def describe(self) -> str:
        """
        Human-readable description of the tensor and its semantic role.
        """
        idx = "".join(self.indices) if self.indices else "·"
        connected = [t.symbol.name for t in self.connections]
        return (
            f"LumerenTensor({self.symbol.name}_{idx}, "
            f"role={self.symbol.role}, connected_to={connected})"
        )


def default_lumeren_symbols() -> Dict[str, LumerenSymbol]:
    """
    Default dictionary of core Luméren symbols used throughout the
    coherence–spacetime framework.
    """
    return {
        "kappa": LumerenSymbol(name="κ", role="coherence", arity=2),
        "tau": LumerenSymbol(name="τ", role="temporal_responsibility", arity=1),
        "sigma": LumerenSymbol(name="Σ", role="systemic_separation", arity=2),
        "evercycle": LumerenSymbol(name="E", role="cosmic_cycle", arity=4),
    }
