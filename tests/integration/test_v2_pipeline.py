from tests.support import WithWorkspace


class PriorComposition(WithWorkspace):
    def test_composition_and_scheduler_files_coexist_with_strategy_archive(self):
        self.cli(cycles=8, overrides={"recursive": {"max_trials": 0}})
        self.assertTrue(self.read_report("scheduling/policy-replay.json")["observed"])
        self.assertTrue(self.read_report("composition/experiments.json"))
        self.assertTrue(self.read_report("recursive_evolution/history.json")["archive"])
