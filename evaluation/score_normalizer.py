import math


def merit(score):
    value = float(score)
    if not math.isfinite(value):
        return 0.0
    return value if value >= 0 else -1 / value
