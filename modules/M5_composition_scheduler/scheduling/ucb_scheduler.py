from math import log, sqrt
from statistics import mean


def choose(arms, samples, exploration=0.8):
    total = 1 + sum(map(len, samples.values()))
    def value(arm):
        values = samples.get(arm, [])
        return mean(values) + exploration * sqrt(log(total) / len(values)) if values else float("inf")
    return max(arms, key=value)
