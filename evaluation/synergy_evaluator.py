from evaluation.score_normalizer import merit
from modules.M5_composition_scheduler.composition.synergy_analyzer import analyze


def evaluate_variants(solver, budget, variants, seeds):
    rows = []
    for seed in seeds:
        scores = {}
        active = {name: path for name, path in variants.items() if path is not None}
        budget.reserve("evaluations", len(active))
        for name, path in active.items():
            budget.check_time()
            result = solver.evaluate(path, seed)
            if not result.valid:
                raise ValueError(f"Invalid composition variant {name}")
            scores[name] = merit(result.score)
        rows.append({"seed": seed, "control": scores["control"],
                     "singles": [score for key, score in scores.items() if key.startswith("single-")],
                     "forward": scores["forward"], "reverse": scores.get("reverse")})
    return analyze(rows)
