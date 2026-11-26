from budget import BudgetError


def reserve_composition(budget, policy_limit):
    if budget.counts.get("composition_trials", 0) >= policy_limit:
        raise BudgetError("Policy composition limit reached")
    budget.reserve("composition_trials")
