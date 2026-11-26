from modules.M6_recursive_evolution.strategy_crossover import crossover
from modules.M6_recursive_evolution.strategy_generator import generate
from modules.M6_recursive_evolution.strategy_mutator import mutate
from tests.support import WithWorkspace


class StrategyGenerator(WithWorkspace):
    def test_builds_patch_and_crossover(self):
        policy = {"step": 0.25, "seed_count": 2}
        suggestion = generate(self.model, policy, [], {"smoke": 2})
        changed = mutate(policy, suggestion)
        self.assertGreater(changed["step"], policy["step"])
        self.assertEqual(crossover(policy, changed)["seed_count"], 2)
