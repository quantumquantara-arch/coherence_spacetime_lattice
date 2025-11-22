import unittest

from src.devices.impossible_devices import (
    DeviceState,
    CoherenceThruster,
    TemporalInductor,
    summarize_device_states,
)
from src.coherence_field import CoherenceMetrics


class TestImpossibleDevices(unittest.TestCase):

    def test_device_state_creation(self):
        state = DeviceState(
            name="thruster_1",
            internal_kappa=0.9,
            internal_tau=0.8,
            internal_sigma=0.1,
        )
        self.assertEqual(state.name, "thruster_1")
        self.assertAlmostEqual(state.internal_kappa, 0.9)
        self.assertAlmostEqual(state.internal_tau, 0.8)
        self.assertAlmostEqual(state.internal_sigma, 0.1)

    def test_coherence_thruster_thrust_index(self):
        state = DeviceState(
            name="thruster",
            internal_kappa=1.0,
            internal_tau=1.0,
            internal_sigma=0.0,
        )
        thruster = CoherenceThruster(state=state)
        thrust = thruster.thrust_index()

        # With κ=1, τ=1, Σ=0 => thrust_index should be 1.0
        self.assertAlmostEqual(thrust, 1.0, places=6)

    def test_temporal_inductor_smoothing_factor(self):
        metrics = CoherenceMetrics(kappa=0.8, tau=0.7, sigma=0.2)
        inductor = TemporalInductor(capacity=2.0, responsibility_bias=1.5)

        smoothing = inductor.smoothing_factor(metrics)

        # Basic sanity checks
        self.assertGreater(smoothing, 0.0)
        # Higher κ/τ and lower Σ should help, but here we just assert it's finite
        self.assertTrue(smoothing < 10.0)

    def test_summarize_device_states(self):
        devices = {
            "A": DeviceState("A", internal_kappa=1.0, internal_tau=1.0, internal_sigma=0.0),
            "B": DeviceState("B", internal_kappa=0.5, internal_tau=0.5, internal_sigma=0.5),
        }

        summary = summarize_device_states(devices)

        self.assertIn("A", summary)
        self.assertIn("B", summary)
        self.assertGreater(summary["A"], summary["B"])  # A is more coherent + responsible


if __name__ == "__main__":
    unittest.main()
