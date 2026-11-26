from tests.support import WithWorkspace


class StrategyRollback(WithWorkspace):
    def test_loss_leaves_prior_checkpoint_active(self):
        self.cli(cycles=2, overrides={"recursive": {
            "trigger_after": 2, "max_trials": 1, "training_attempts": 1, "minimum_gain": 1.0}})
        report = self.read_report("recursive_evolution/history.json")
        trial, = report["trials"]
        self.assertFalse(trial["accepted"])
        self.assertEqual(report["active"], trial["previous"])
        self.assertIn(trial["challenger"], report["archive"])
