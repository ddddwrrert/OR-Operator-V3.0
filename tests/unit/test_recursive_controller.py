from modules.M6_recursive_evolution.evolution_trigger import triggered
from modules.M6_recursive_evolution.strategy_selector import choose
from unittest import TestCase


class RecursiveController(TestCase):
    def test_trigger_and_conservative_promotion(self):
        flags = [i for i in range(10) if triggered(i, {"trigger_after": 2, "interval": 3})]
        self.assertEqual(flags, [2, 5, 8])
        self.assertFalse(choose({"mean_gain": 2, "positive_fraction": 0.75, "worst_gain": -1}, 0.01))
        self.assertTrue(choose({"mean_gain": 2, "positive_fraction": 0.75, "worst_gain": 0}, 0.01))
