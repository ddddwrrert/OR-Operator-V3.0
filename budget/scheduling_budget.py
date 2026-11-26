def exploration_allowed(budget):
    return budget.remaining_evaluations() >= 2
