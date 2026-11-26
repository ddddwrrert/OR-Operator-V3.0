from budget.seed_budget import allocate
from .compiler_checker import compile_candidate
from .contribution_analyzer import contribution
from .cost_benefit_analyzer import cost_benefit
from .feasibility_checker import feasible
from .paired_seed_evaluator import evaluate_pair
from .robustness_analyzer import robustness
from .smoke_test import smoke
from .static_checker import check_scope


def validate(solver, budget, parent, candidate, config):
    check_scope(parent.read_text(encoding="utf-8"), candidate.read_text(encoding="utf-8"))
    budget.check_time()
    compile_candidate(solver, candidate)
    seeds = allocate(config["seeds"])
    if not solver.supports_seeds:
        seeds = seeds[:1]
    first = smoke(solver, budget, parent, candidate, seeds[0])
    pairs = [first]
    if not feasible(first) or first["gain"] <= 0:
        stage = "smoke"
    else:
        stage = "paired" if solver.supports_seeds else "single-evaluation"
        for seed in seeds[1:]:
            pair = evaluate_pair(solver, budget, parent, candidate, seed)
            pairs.append(pair)
            if not feasible(pair):
                break
    attribution = contribution(pairs)
    stability = robustness(pairs)
    accepted = (len(pairs) == len(seeds) and all(feasible(pair) for pair in pairs)
                and attribution["gain"] > config["minimum_gain"]
                and stability["positive_fraction"] >= config["majority"])
    return {"stage": stage, "accepted": accepted, "pairs": pairs,
            **attribution, **stability, **cost_benefit(pairs, attribution["gain"])}
