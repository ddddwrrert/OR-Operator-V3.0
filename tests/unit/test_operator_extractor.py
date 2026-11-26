from modules.M1_operator_profiler import build_profile
from unittest import TestCase


class ExtractorTest(TestCase):
    def test_finds_search_inside_loop_without_named_operator(self):
        source = "#EVOLVE_START\nfor i in range(4):\n    state[i] = improve(state[i])\n#EVOLVE_END\n"
        profile = build_profile(source, "solution.py", [])
        update = next(item for item in profile["operators"] if item["location"] == "<inline>")
        self.assertIn("state[i]", update["writes"])
        self.assertEqual(update["kind"], "iterative-state-update")
