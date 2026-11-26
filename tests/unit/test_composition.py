from modules.M5_composition_scheduler.composition.operator_sequence_generator import sequences
from unittest import TestCase


def move(name, offset, before=()):
    return {"name": name, "writes": [f"state[{offset}]"], "before": before}


class Composition(TestCase):
    def test_chain_enforces_order_and_length(self):
        a, b, c = move("a", 0, ["b"]), move("b", 0), move("c", 1)
        result = sequences([a, b, c], 3)
        self.assertIn((a, b, c), result)
        self.assertNotIn((b, a), result)
        self.assertTrue(all(len(item) == 2 for item in sequences([a, b, c], 2)))
