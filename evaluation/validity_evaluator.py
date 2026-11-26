import math


def valid(score, metrics):
    return (isinstance(score, (int, float)) and not isinstance(score, bool)
            and math.isfinite(score) and score != 0 and not metrics.get("error")
            and not metrics.get("timeout") and metrics.get("feasible", True) is not False)
