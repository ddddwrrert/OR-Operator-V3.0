from tests.support import WithWorkspace


class MetaPipeline(WithWorkspace):
    def test_one_probe_has_matched_independent_holdout(self):
        result = self.cli(cycles=2, overrides={"recursive": {
            "trigger_after": 2, "max_trials": 1, "training_attempts": 1}})
        trial, = self.read_report("recursive_evolution/history.json")["trials"]
        self.assertEqual(result["budget_used"]["meta_trials"], 1)
        self.assertEqual(len(trial["pairs"]), 4)
        self.assertEqual({pair["seed"] for pair in trial["pairs"]}, {101, 307})
