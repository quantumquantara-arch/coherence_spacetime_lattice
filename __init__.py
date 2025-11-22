"""
coherence_spacetime_lattice package initialization.

Exposes the primary classes for:
- CoherenceField (κ–τ–Σ field)
- SpacetimeLattice (discrete coherence-spacetime grid)
- TemporalEngineVeyn (temporal coherence engine)
- LumerenSymbol / LumerenTensor (symbolic–geometric tensor language)
"""

from .coherence_field import CoherenceField, CoherenceMetrics
from .spacetime_lattice import SpacetimeLattice
from .temporal_engine_veyn import TemporalEngineVeyn, TemporalChannel
from .lumeren_tensor import LumerenSymbol, LumerenTensor, default_lumeren_symbols
