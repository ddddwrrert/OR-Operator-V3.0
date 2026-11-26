from meta.budget_strategy.resource_allocation import can_probe


def available(budget, required, limit):
    return budget.counts.get("meta_trials", 0) < limit and can_probe(budget, required)
