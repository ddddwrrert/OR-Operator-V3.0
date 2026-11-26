from modules.M3_operator_discovery.operator_design_reasoner import select
from modules.M3_operator_discovery.operator_spec_generator import specification
from unittest import TestCase


class DiscoveryTest(TestCase):
    def test_uses_open_vocabulary_and_structured_state(self):
        candidate = {"name": "Novel structural move", "rationale": "measured residual", "writes": ["state"]}
        self.assertEqual(specification(select([{}, candidate]), "state = 1").writes, ("state",))
        with self.assertRaises(ValueError):
            specification(dict(candidate, writes="state"), "state = 1")
