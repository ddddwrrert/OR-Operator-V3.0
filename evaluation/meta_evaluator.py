from interfaces.meta_evolution_interface import StrategyEvaluator
from meta.validation_strategy.experiment_selection import matched_jobs
from meta.validation_strategy.statistical_policy import summarize
from .strategy_evaluator import evaluate_strategy


def compare(engine, control, challenger, config, evaluate: StrategyEvaluator = evaluate_strategy):
    tasks = [tuple(task) for task in config["tasks"]]
    jobs = matched_jobs(tasks, config["heldout_seeds"])
    left, right = {}, {}
    for target in tasks:
        left[target] = evaluate(engine, target, control, config)
        right[target] = evaluate(engine, target, challenger, config)
    pairs = [{"task": target, "seed": seed, "control": left[target][seed],
              "challenger": right[target][seed]} for target, seed in jobs]
    return pairs, summarize(pairs)
