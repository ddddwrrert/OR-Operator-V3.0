from execution.strategy_executor import execute


def evaluate_strategy(engine, target, policy, config):
    return execute(engine, target, policy, config["training_seed"],
                   config["heldout_seeds"], config["training_attempts"])
