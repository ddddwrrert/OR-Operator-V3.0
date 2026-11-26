from modules.M3_operator_discovery import discover
from tests.support import WithWorkspace


class Discovery(WithWorkspace):
    def test_ordered_component_metadata_selects_an_actual_edit(self):
        result = discover(self.model, self.solver.baseline, self.diagnosis(), self.profile(), {},
                          {"components": [{"metadata": {"coordinate": 1}}]})
        self.assertIn("WEIGHTS[1]", result.writes)
        self.assertIn("-0.5", result.body)
