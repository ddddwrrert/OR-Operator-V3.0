from tests.support import WithWorkspace


class RollbackTest(WithWorkspace):
    def test_failed_gain_keeps_incumbent_and_rejection(self):
        result = self.cli(cycles=2, overrides={"evaluation": {"minimum_gain": 1.0}})
        self.assertEqual(result["incumbent"], "000000")
        self.assertEqual(result["accepted"], 0)
        self.assertTrue((self.work / "run/storage/rejected/000001/solver.py").is_file())
