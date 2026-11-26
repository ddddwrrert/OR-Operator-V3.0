from modules.M3_operator_discovery import discover
from tests.support import WithWorkspace


class Integration(WithWorkspace):
    def test_diagnosis_generates_real_source_body(self):
        op = discover(self.model, self.solver.baseline, self.diagnosis(), self.profile(), {"step": 0.5}, None)
        self.assertIn("1.5", op.body)
        self.assertIn("WEIGHTS[0]", op.writes)
