import unittest
import numpy as np

from src.coherence_field import CoherenceField


class TestCoherenceField(unittest.TestCase):
    def test_initialization(self):
        field = CoherenceField(10, 10)
        self.assertEqual(field.kappa.shape, (10, 10))
        self.assertEqual(field.tau.shape, (10, 10))
        self.assertEqual(field.sigma.shape, (10, 10))
        self.assertTrue(np.allclose(field.kappa, 0.0))
        self.assertTrue(np.allclose(field.tau, 0.0))
        self.assertTrue(np.allclose(field.sigma, 0.0))

    def test_center_pulse(self):
        field = CoherenceField(5, 5)
        field.initialize_center_pulse(radius=1, kappa_peak=1.0, tau_value=1.0, sigma_value=0.0)
        cy, cx = 2, 2
        self.assertAlmostEqual(field.kappa[cy, cx], 1.0, places=6)
        self.assertAlmostEqual(field.tau[cy, cx], 1.0, places=6)
        self.assertAlmostEqual(field.sigma[cy, cx], 0.0, places=6)

    def test_step_changes_state_and_preserves_bounds(self):
        field = CoherenceField(40, 40)
        field.initialize_center_pulse()
        k0 = field.kappa.copy()
        field.step_local_dynamics(dt=0.08)
        self.assertFalse(np.allclose(k0, field.kappa))
        self.assertGreaterEqual(field.kappa.min(), 0.0)
        self.assertLessEqual(field.kappa.max(), 1.0)
        self.assertGreaterEqual(field.tau.min(), 0.0)
        self.assertLessEqual(field.tau.max(), 1.0)
        self.assertGreaterEqual(field.sigma.min(), 0.0)

    def test_free_energy_finite(self):
        field = CoherenceField(30, 30)
        field.randomize(seed=0)
        F = field.coherence_free_energy()
        self.assertTrue(np.isfinite(F))


if __name__ == "__main__":
    unittest.main()
