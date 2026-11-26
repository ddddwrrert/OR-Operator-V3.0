from tests.support import WithWorkspace


class Diagnosis(WithWorkspace):
    def test_reports_evidence_confidence_and_verification(self):
        diagnosis = self.diagnosis()
        self.assertGreater(diagnosis.confidence, 0.5)
        self.assertGreaterEqual(len(diagnosis.evidence), 2)
        self.assertIn("matched", diagnosis.test)
