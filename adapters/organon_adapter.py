import json
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from adapters.cpp_solver_adapter import CppSolverAdapter
from execution.process_runner import run
from execution.sandbox import require_isolation
from interfaces.evaluator_interface import Outcome


class OrganonAdapter:
    def __init__(self, checkout, task, workspace, config):
        checkout, task, workspace = (Path(item).resolve() for item in (checkout, task, workspace))
        if workspace == checkout or workspace.is_relative_to(checkout):
            raise ValueError("Use a working directory outside original Organon")
        runner = checkout / "plugins/dsh-evolve-loop/src/providers/run_evaluator.py"
        if not runner.is_file():
            raise ValueError("Original Organon evaluator runner is missing")
        self.prefix = require_isolation(config.get("sandbox_prefix", []))
        self.task = workspace / "storage" / "task"
        settings = json.loads((task / "task.json").read_text(encoding="utf-8"))
        self.program = settings["program"]
        if Path(self.program).name != self.program:
            raise ValueError("Task program must be a filename")
        if not self.task.exists():
            shutil.copytree(task, self.task, ignore=shutil.ignore_patterns("run", "__pycache__"))
        elif (self.task / "task.json").read_bytes() != (task / "task.json").read_bytes():
            raise ValueError("Task settings changed. Use a new workspace.")
        self.runner = self.task.parent / "run_organon_evaluator.py"
        shutil.copyfile(runner, self.runner)
        self.baseline = (self.task / self.program).read_text(encoding="utf-8")
        self.timeout = config.get("timeout", 10)
        self.seed_env = config.get("organon_seed_env", "")
        self.supports_seeds = bool(self.seed_env)
        self.compiler = CppSolverAdapter(config.get("compiler", "g++"), self.timeout, self.prefix)
        self.env = settings.get("env", {})

    def check(self, source):
        self.compiler.check(source)

    def evaluate(self, source, seed):
        from evaluation.validity_evaluator import valid
        with TemporaryDirectory(dir=source.parent) as tmp:
            env = {**self.env, "TMPDIR": tmp, "TMP": tmp, "TEMP": tmp}
            if self.seed_env:
                env[self.seed_env] = str(seed)
            result = run([sys.executable, "-B", str(self.runner), str(self.task), str(source)],
                         cwd=self.task / "evaluator", timeout=self.timeout,
                         prefix=self.prefix, env=env).require_success()
        value = json.loads(result.stdout.strip().splitlines()[-1])
        return Outcome(value["fitness"], result.seconds, valid(value["fitness"], value["metrics"]),
                       value["metrics"])
