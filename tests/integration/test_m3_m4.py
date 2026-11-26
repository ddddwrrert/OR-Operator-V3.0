from budget import Budget
from execution.code_workspace import write_candidate
from modules.M3_operator_discovery import discover
from modules.M3_operator_discovery.candidate_manager import prepare
from modules.M4_operator_validation import validate
from tests.support import WithWorkspace


class Integration(WithWorkspace):
    def test_executes_generated_candidate_on_matched_instances(self):
        base = write_candidate(self.work, "000000", self.solver.program, self.solver.baseline)
        proposal = discover(self.model, self.solver.baseline, self.diagnosis(), self.profile(), {}, None)
        candidate = prepare(self.work, self.solver, {"id": "000001", "parent": "000000"},
                            proposal, self.solver.baseline, [])
        budget = Budget({"evaluations": 6, "runtime_seconds": 60}, {}, lambda: None)
        result = validate(self.solver, budget, base, candidate,
                          {"seeds": [11, 29, 47], "minimum_gain": 0.0, "majority": 0.6})
        self.assertTrue(result["accepted"])
        self.assertEqual(len(result["pairs"]), 3)
