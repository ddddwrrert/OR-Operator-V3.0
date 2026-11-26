from tests.support import WithWorkspace


class RecursiveDiscovery(WithWorkspace):
    def test_trial_keeps_original_enforcement_and_creates_new_policy(self):
        result = self.cli(cycles=2, overrides={"recursive": {
            "trigger_after": 2, "training_attempts": 1}, "budget": {"candidates": 2}})
        report = self.read_report("recursive_evolution/history.json")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(len(report["archive"]), 2)
