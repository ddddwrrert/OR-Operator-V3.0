from .paired_seed_evaluator import evaluate_pair


def smoke(solver, budget, parent, candidate, seed):
    return evaluate_pair(solver, budget, parent, candidate, seed)
