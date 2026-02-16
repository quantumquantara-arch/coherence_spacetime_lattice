import unittest
import numpy as np
from src.coherence_field import CoherenceParams

class TestJacobianStability(unittest.TestCase):
    def test_trace_negative_at_equilibrium(self):
        p = CoherenceParams()
        k,t,s = 0.5,0.5,0.1
        J11 = p.a_kappa*t*(1-2*k) - p.lambda_kappa*s
        J33 = -p.lambda_sigma
        self.assertTrue(J33 < 0)
