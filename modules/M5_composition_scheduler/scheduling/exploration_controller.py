from budget.scheduling_budget import exploration_allowed


def available(operators, sequence, budget):
    arms = ["discover"]
    if operators and exploration_allowed(budget):
        arms.append("reuse")
    if sequence and exploration_allowed(budget):
        arms.append("compose")
    return arms
