from meta.validation_strategy.acceptance_policy import promote


def choose(summary, minimum_gain):
    return promote(summary, minimum_gain)
