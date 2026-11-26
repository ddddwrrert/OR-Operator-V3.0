from tests.support import WithWorkspace


class MetaEvolution(WithWorkspace):
    def test_meta_budget_blocks_trials_with_no_probe_allowance(self):
        result = self.cli(cycles=3, overrides={"recursive": {"max_trials": 0}})
        self.assertNotIn("meta_trials", result["budget_used"])
        self.assertEqual(self.read_report("recursive_evolution/history.json")["trials"], [])
