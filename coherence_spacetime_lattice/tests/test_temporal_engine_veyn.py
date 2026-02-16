import unittest

from temporal.temporal_engine_veyn import TemporalEngineVeyn, TemporalChannel
from src.coherence_field import CoherenceMetrics


class TestTemporalEngineVeyn(unittest.TestCase):
    def test_channel_addition(self):
        ch = TemporalChannel(name="test")
        ch.add(CoherenceMetrics(kappa=1.0, tau=0.5, sigma=0.2))
        self.assertEqual(len(ch.sequence), 1)

    def test_channel_averages(self):
        ch = TemporalChannel(name="avg_test")
        ch.add(CoherenceMetrics(1.0, 0.5, 0.3))
        ch.add(CoherenceMetrics(0.5, 0.3, 0.1))
        self.assertAlmostEqual(ch.average_kappa(), 0.75, places=6)
        self.assertAlmostEqual(ch.average_tau(), 0.4, places=6)
        self.assertAlmostEqual(ch.average_sigma(), 0.2, places=6)

    def test_temporal_responsibility_score(self):
        ch = TemporalChannel(name="score_test")
        ch.add(CoherenceMetrics(kappa=1.0, tau=1.0, sigma=0.0))
        score = ch.temporal_responsibility_score()
        self.assertGreater(score, 0.9)

    def test_engine_ranking(self):
        ch1 = TemporalChannel(name="A")
        ch1.add(CoherenceMetrics(1.0, 1.0, 0.2))
        ch2 = TemporalChannel(name="B")
        ch2.add(CoherenceMetrics(0.3, 0.4, 0.9))
        engine = TemporalEngineVeyn()
        engine.add_channel(ch1)
        engine.add_channel(ch2)
        ranked = engine.rank_channels_by_responsibility()
        self.assertEqual(ranked[0].name, "A")
        self.assertEqual(ranked[-1].name, "B")


if __name__ == "__main__":
    unittest.main()
