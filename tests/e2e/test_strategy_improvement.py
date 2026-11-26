from tests.support import WithWorkspace


class StrategyImprovement(WithWorkspace):
    def test_fixed_seed_improvement_changes_active_strategy(self):
        self.cli(cycles=2, overrides={"recursive": {
            "trigger_after": 2, "training_attempts": 1, "max_trials": 1}})
        report = self.read_report("recursive_evolution/history.json")
        trial, = report["trials"]
        self.assertTrue(trial["accepted"])
        self.assertGreater(trial["summary"]["mean_gain"], 0)
        self.assertEqual(report["active"], trial["challenger"])
