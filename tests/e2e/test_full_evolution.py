from pathlib import Path
from tests.support import WithWorkspace


class EvolutionTest(WithWorkspace):
    def test_command_evolves_and_archives(self):
        result = self.cli()
        self.assertEqual(result["attempts"], 4)
        self.assertGreater(result["accepted"], 0)
        self.assertTrue(Path(result["solver"]).is_file())
        memory = self.read_report("final/memory.json")
        self.assertEqual(len(memory["operators"]), 4)
