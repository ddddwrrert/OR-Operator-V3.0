from tests.support import WithWorkspace


class FullVersion(WithWorkspace):
    def test_cli_reports_candidates_scheduler_and_strategy(self):
        result = self.cli(cycles=3, overrides={"recursive": {"max_trials": 0}})
        self.assertEqual(result["version"], "3.0")
        self.assertGreater(result["accepted"], 0)
        self.assertTrue(self.read_report("scheduling/policy-replay.json")["decisions"])
        self.assertTrue(self.read_report("recursive_evolution/history.json")["active"])
