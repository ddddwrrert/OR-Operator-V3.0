from functools import partial
from interfaces.scheduler_interface import Scheduler
from . import thompson_scheduler, ucb_scheduler


def choose(algorithm, arms, samples, config, seed):
    if algorithm == "Thompson":
        scheduler: Scheduler = partial(thompson_scheduler.choose, seed=seed)
    elif algorithm == "UCB":
        scheduler = partial(ucb_scheduler.choose, exploration=config["exploration"])
    else:
        raise ValueError("Scheduler must be UCB or Thompson")
    return scheduler(arms, samples)
