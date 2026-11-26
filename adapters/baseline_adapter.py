import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import math
from adapters.instance_adapter import expected, instances
from execution.code_integrator import executable
from execution.compiler import check
from execution.process_runner import run
from interfaces.evaluator_interface import Outcome


def demo_body(weights):
    return (
        f"WEIGHTS = {list(weights)!r}\n\n"
        "def predict(row):\n"
        "    score = 0.0\n"
        "    for weight, feature in zip(WEIGHTS, row, strict=True):\n"
        "        score += weight * feature\n"
        "    return score"
    )


class Baseline:
    program = "solver.py"
    supports_seeds = True

    def __init__(self, target, timeout=5):
        self.target = tuple(target)
        self.timeout = timeout
        self.baseline = (
            "#EVOLVE_START\n" + demo_body([0.0] * len(target)) +
            "\n#EVOLVE_END\n\nif __name__ == '__main__':\n"
            "    import json, sys, time\n"
            "    rows = json.loads(sys.argv[1])\n"
            "    started = time.perf_counter()\n"
            "    predictions = [predict(row) for row in rows]\n"
            "    elapsed = time.perf_counter() - started\n"
            "    print(json.dumps({'predictions': predictions, 'predict_seconds': elapsed}))\n"
        )

    def check(self, source):
        check(source)

    def evaluate(self, source, seed):
        rows = instances(self.target, seed)
        with TemporaryDirectory(dir=source.parent) as tmp:
            program = Path(tmp) / self.program
            program.write_text(executable(source.read_text(encoding="utf-8")), encoding="utf-8")
            result = run([sys.executable, "-I", "-B", str(program), json.dumps(rows)],
                         cwd=tmp, timeout=self.timeout).require_success()
        output = json.loads(result.stdout)
        predictions = output["predictions"]
        if not isinstance(predictions, list) or len(predictions) != len(rows):
            return Outcome(0, result.seconds, False, {"reason": "prediction shape"})
        mse = sum((p - expected(row, self.target)) ** 2
                  for row, p in zip(rows, predictions, strict=True)) / len(rows)
        return Outcome(1 / (1 + mse), result.seconds, math.isfinite(mse), {
            "mse": mse, "operators": {"predict": {"calls": len(rows), "seconds": output["predict_seconds"]}},
        })
