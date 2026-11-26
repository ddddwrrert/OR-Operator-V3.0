import os
import sys
from pathlib import Path
from adapters.organon_adapter import OrganonAdapter
from execution.code_workspace import write_candidate
from tests.support import PROJECT, WithWorkspace


class OrganonTest(WithWorkspace):
    def test_evaluator_uses_staged_task_copy(self):
        original = Path(os.environ.get("ORGANON_ROOT", PROJECT.parents[1] / "Organon\uff08\u539f\uff09"))
        if not original.is_dir():
            self.skipTest("Set ORGANON_ROOT to test the original evaluator")
        fixture = original / "plugins/dsh-evolve-loop/tests/fixtures/task"
        baseline = (fixture / "solution.py").read_bytes()
        prefix = self.work / "trusted_fixture_launcher.py"
        prefix.write_text("import subprocess, sys\nraise SystemExit(subprocess.call(sys.argv[1:]))", encoding="utf-8")
        adapter = OrganonAdapter(original, fixture, self.work,
                                 {"sandbox_prefix": [sys.executable, str(prefix)], "timeout": 15})
        item = write_candidate(self.work, "000000", adapter.program, adapter.baseline)
        self.assertEqual(adapter.evaluate(item, 11).score, 10)
        self.assertEqual((fixture / "solution.py").read_bytes(), baseline)
        self.assertNotEqual(fixture.resolve(), adapter.task.resolve())
