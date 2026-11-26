from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
from adapters.baseline_adapter import Baseline
from adapters.model import DemoModel
from budget.seed_budget import allocate
from evaluation.score_normalizer import merit
from execution.code_integrator import integrate
from meta.composition_strategy.interaction_search import eligible
from modules.M1_operator_profiler import build_profile
from modules.M2_bottleneck_diagnosis import diagnose
from modules.M3_operator_discovery import discover


def execute(engine, target, policy, training_seed, heldout, attempts):
    solver = Baseline(target, engine.config["solver"]["timeout"])
    backend = DemoModel(target)
    current = solver.baseline
    history = []
    operators = {}
    folder = engine.workspace / "storage" / "strategy_checkpoints"
    folder.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=folder) as temporary:
        work = Path(temporary)
        def evaluate(source, seed, name):
            engine.budget.reserve("evaluations")
            path = work / (name + ".py")
            path.write_text(source, encoding="utf-8")
            outcome = solver.evaluate(path, seed)
            if not outcome.valid:
                raise ValueError("Invalid fixed-task output")
            return merit(outcome.score)

        for i in range(attempts):
            profile = build_profile(current, solver.program, history)
            diagnosis = diagnose(backend, current, profile, history, policy)
            if not diagnosis or diagnosis.confidence < policy["confidence"]:
                continue
            orders = eligible(list(operators.values()), policy["max_sequence"])
            compose = bool(orders) and policy["composition_limit"] > 0
            plan = {"kind": "compose", "components": max(orders, key=len)} if compose else None
            operator = discover(backend, current, diagnosis, profile, policy, plan)
            candidate = integrate(current, operator.body)
            validation = []
            for j, seed in enumerate(allocate([training_seed + n for n in range(policy["seed_count"])])):
                validation.append(evaluate(candidate, seed, f"candidate-{i}-{j}")
                                  - evaluate(current, seed, f"control-{i}-{j}"))
            accepted = all(value >= 0 for value in validation) and any(value > 0 for value in validation)
            item = {key: value for key, value in asdict(operator).items() if key != "body"}
            if accepted:
                current = candidate
                if not compose:
                    operators[item["name"]] = item
            history.append({"id": str(i), "operator": item, "accepted": accepted,
                            "gain": sum(validation) / len(validation)})
        return {seed: evaluate(current, seed, f"heldout-{i}") for i, seed in enumerate(heldout)}
