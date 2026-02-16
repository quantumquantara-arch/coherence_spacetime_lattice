import unittest
import numpy as np

from spacetime.spacetime_lattice import SpacetimeLattice


class TestSpacetimeLattice(unittest.TestCase):
    def test_initialization(self):
        lattice = SpacetimeLattice(10, 10)
        self.assertEqual(lattice.field.height, 10)
        self.assertEqual(lattice.field.width, 10)
        self.assertEqual(lattice.time_step, 0)
        self.assertEqual(len(lattice.history), 0)

    def test_center_pulse(self):
        lattice = SpacetimeLattice(5, 5)
        lattice.initialize_center_pulse()
        cy, cx = 2, 2
        m = lattice.field.get_metrics(cy, cx)
        self.assertAlmostEqual(m.kappa, 1.0, places=6)

    def test_step_and_geometry(self):
        lattice = SpacetimeLattice(40, 40)
        lattice.initialize_center_pulse()
        lattice.step(dt=0.08)
        self.assertEqual(lattice.time_step, 1)
        self.assertEqual(len(lattice.history), 1)
        self.assertEqual(len(lattice.geometry_history), 1)
        snap = lattice.snapshot()
        self.assertIn("curvature_proxy", snap)
        self.assertTrue(np.isfinite(snap["curvature_proxy"]).all())


if __name__ == "__main__":
    unittest.main()
