def available_tokens(budget):
    return max(0, budget.limits["tokens"] - budget.counts.get("tokens", 0))
