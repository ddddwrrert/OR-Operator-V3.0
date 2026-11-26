from tests.support import WithWorkspace


class Integration(WithWorkspace):
    def test_profiles_state_and_produces_falsifiable_diagnosis(self):
        self.assertIn("predict", self.profile()["graph"])
        result = self.diagnosis()
        self.assertIn("Coordinate", result.claim)
        self.assertGreater(result.confidence, 0.6)
