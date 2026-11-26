from tests.support import WithWorkspace


class PriorPipeline(WithWorkspace):
    def test_strategy_aware_pipeline_keeps_validation_stages(self):
        self.cli(cycles=1)
        stored = self.read_report("experiment/000001.json")
        self.assertIn("diagnosis", stored)
        self.assertEqual(stored["stage"], "paired")
