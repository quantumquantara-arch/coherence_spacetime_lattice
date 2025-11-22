import unittest
import numpy as np

from src.spacetime_lattice import SpacetimeLattice


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

        metrics = lattice.field.get_metrics(cy, cx)
        self.assertAlmostEqual(metrics.kappa, 1.0, places=6)
        self.assertAlmostEqual(metrics.tau, 0.5, places=6)
        self.assertAlmostEqual(metrics.sigma, 0.1, places=6)

    def test_single_step(self):
        lattice = SpacetimeLattice(5, 5)
        lattice.initialize_center_pulse()

        lattice.step()  # default dynamics
        self.assertEqual(lattice.time_step, 1)
        self.assertEqual(len(lattice.history), 1)

        metrics = lattice.history[0]
        self.assertGreaterEqual(metrics.kappa, 0.0)
        self.assertGreaterEqual(metrics.tau, 0.0)
        self.assertGreaterEqual(metrics.sigma, 0.0)

    def test_run_multiple_steps(self):
        lattice = SpacetimeLattice(5, 5)
        lattice.initialize_center_pulse()

        lattice.run(steps=10)
        self.assertEqual(lattice.time_step, 10)
        self.assertEqual(len(lattice.history), 10)


if __name__ == "__main__":
    unittest.main()
