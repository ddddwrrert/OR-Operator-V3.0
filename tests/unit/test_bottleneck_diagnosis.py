from modules.M2_bottleneck_diagnosis.confidence_estimator import estimate
from modules.M2_bottleneck_diagnosis.hypothesis_verifier import verifiable
from unittest import TestCase


class DiagnosisTest(TestCase):
    def test_open_claim_and_falsification_required(self):
        self.assertTrue(verifiable("Unseen double-transition bottleneck", ["trace"], "paired ablation"))
        self.assertFalse(verifiable("claim", [], "paired ablation"))
        self.assertEqual(estimate(0.99, ["only one observation"]), 0.9)
        with self.assertRaises(ValueError):
            estimate(float("nan"), ["x"])
