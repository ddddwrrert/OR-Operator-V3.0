from modules.M5_composition_scheduler.scheduling.scheduler_controller import choose
from unittest import TestCase


class Scheduler(TestCase):
    def test_selects_consistent_contextual_policy(self):
        samples = {"base": [0.5]}
        for algorithm in ("UCB", "Thompson"):
            self.assertEqual(choose(algorithm, ["base", "unused"], samples, {"exploration": 0.7}, 3), "unused")
