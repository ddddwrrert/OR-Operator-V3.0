def can_probe(budget, jobs):
    return budget.remaining_evaluations() >= jobs
