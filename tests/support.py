import json
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from adapters.baseline_adapter import Baseline
from adapters.model import DemoModel
from config import load
from modules.M1_operator_profiler import build_profile
from modules.M2_bottleneck_diagnosis import diagnose

PROJECT = Path(__file__).resolve().parents[1]


class WithWorkspace(TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name)
        self.solver = Baseline([3, -2, 1])
        self.model = DemoModel(self.solver.target)

    def profile(self):
        return build_profile(self.solver.baseline, self.solver.program, [])

    def diagnosis(self):
        return diagnose(self.model, self.solver.baseline, self.profile(), [], {"window": 6})

    def cli(self, *, cycles=4, overrides=None):
        config = self.work / "override.json"
        config.write_text(json.dumps({"cycles": cycles, **(overrides or {})}), encoding="utf-8")
        work = self.work / "run"
        result = subprocess.run([sys.executable, "-B", str(PROJECT / "run.py"), "--work", str(work),
                                 "--config", str(config)], cwd=self.work, capture_output=True,
                                text=True, encoding="utf-8", timeout=160, check=False,
                                env={**os.environ, "PYTHONUTF8": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def read_report(self, subpath):
        return json.loads((self.work / "run" / "reports" / subpath).read_text(encoding="utf-8"))
