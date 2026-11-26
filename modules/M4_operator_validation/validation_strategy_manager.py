from meta.validation_strategy.seed_allocation import seed_count


def options(policy, config):
    return {"seed_count": seed_count(policy["seed_count"], len(config["evaluation"]["seeds"]))}
