from tests.support import WithWorkspace


class Resume(WithWorkspace):
    def test_invoking_completed_run_preserves_budget_and_solver(self):
        first = self.cli(cycles=3, overrides={"recursive": {"max_trials": 0}})
        again = self.cli(cycles=3, overrides={"recursive": {"max_trials": 0}})
        self.assertEqual(first["budget_used"], again["budget_used"])
        self.assertEqual(first["incumbent"], again["incumbent"])
