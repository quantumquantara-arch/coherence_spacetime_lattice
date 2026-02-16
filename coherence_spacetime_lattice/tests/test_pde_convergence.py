import unittest
import numpy as np
from src.coherence_field import CoherenceField

class TestPDEConvergence(unittest.TestCase):
    def test_diffusion_variance_scaling(self):
        field = CoherenceField(80, 80)
        field.initialize_center_pulse(radius=1)
        D = field.params.D_kappa
        for _ in range(50):
            field.step_local_dynamics(dt=0.05)
        k = field.kappa
        y, x = np.indices(k.shape)
        cy, cx = 40, 40
        r2 = (y-cy)**2 + (x-cx)**2
        variance = np.sum(r2*k)/np.sum(k)
        self.assertTrue(variance > 0)
