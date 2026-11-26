from budget import Budget, BudgetError
from unittest import TestCase


class BudgetTest(TestCase):
    def test_reservations_survive_reopen_and_cannot_overspend(self):
        snapshots = []
        limits = {"runtime_seconds": 100, "evaluations": 3}
        state = {}
        budget = Budget(limits, state, lambda: snapshots.append(state["budget"].copy()))
        budget.reserve("evaluations", 2)
        resumed = Budget(limits, state, lambda: None)
        with self.assertRaises(BudgetError):
            resumed.reserve("evaluations", 2)
        self.assertEqual(snapshots, [{"evaluations": 2}])
        self.assertEqual(resumed.remaining_evaluations(), 1)
