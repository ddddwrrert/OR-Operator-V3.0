from budget.meta_evolution_budget import available
from meta.budget_strategy.token_allocation import available_tokens


def can_evolve(budget, required, config):
    return available(budget, required, config["max_trials"]) and available_tokens(budget) > 0
