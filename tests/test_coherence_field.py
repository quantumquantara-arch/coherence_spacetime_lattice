import unittest
import numpy as np

from src.coherence_field import CoherenceField

class TestCoherenceField(unittest.TestCase):

    def test_initialization(self):
        field = CoherenceField(10, 10)
        kappa = field.kappa
        tau = field.tau
        sigma = field.sigma

        self.assertEqual(kappa.shape, (10, 10))
        self.assertEqual(tau.shape, (10, 10))
        self.assertEqual(sigma.shape, (10, 10))

    def test_center_pulse(self):
        field = CoherenceField(5, 5)
        field.initialize_center_pulse()

        cx, cy = 2, 2
        self.assertAlmostEqual(field.kappa[cx, cy], 1.0, places=6)
        self.assertAlmostEqual(field.tau[cx, cy], 1.0, places=6)
        self.assertAlmostEqual(field.sigma[cx, cy], 0.0, places=6)

    def test_step_local_dynamics(self):
        field = CoherenceField(5, 5)
        field.initialize_center_pulse()

        before = field.kappa.copy()
        field.step_local_dynamics()

        # Verify something changed
        self.assertFalse(np.allclose(before, field.kappa))

if __name__ == "__main__":
    unittest.main()
