from evaluation.meta_evaluator import compare
from .strategy_sandbox import sandbox


def validate(engine, incumbent, challenger, config):
    control = sandbox(incumbent, engine.config)
    treatment = sandbox(challenger, engine.config)
    return compare(engine, control, treatment, config)
