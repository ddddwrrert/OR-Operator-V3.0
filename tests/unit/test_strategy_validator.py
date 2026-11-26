from config import load
from modules.M6_recursive_evolution.strategy_sandbox import sandbox
from unittest import TestCase


class StrategySandbox(TestCase):
    def test_refuses_executable_or_budget_overrides(self):
        config = load()
        for patch in ({"code": "print(1)"}, {"composition_limit": 500}, {"step": 10}, {"seed_count": 500}):
            with self.assertRaises(ValueError):
                sandbox(patch, config)
        result = sandbox({"window": 4}, config)
        self.assertEqual(result["window"], 4)
        with self.assertRaises(TypeError):
            result["window"] = 20
