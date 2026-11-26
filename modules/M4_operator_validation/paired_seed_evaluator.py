from evaluation.paired_comparison import compare


def evaluate_pair(solver, budget, parent, candidate, seed):
    budget.reserve("evaluations", 2)
    control = solver.evaluate(parent, seed)
    result = solver.evaluate(candidate, seed)
    return compare(seed, control, result)
