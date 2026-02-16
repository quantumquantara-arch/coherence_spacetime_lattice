import unittest
import numpy as np
from spacetime.spacetime_lattice import SpacetimeLattice

class TestGeometryConsistency(unittest.TestCase):
    def test_flat_state_zero_curvature(self):
        lattice = SpacetimeLattice(40,40)
        lattice.field.kappa[:] = 0.5
        R = lattice.curvature_proxy()
        self.assertTrue(np.allclose(R,0,atol=1e-6))
