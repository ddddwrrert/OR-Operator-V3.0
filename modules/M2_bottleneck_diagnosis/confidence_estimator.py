import math


def estimate(raw, evidence):
    value = float(raw)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("Confidence must be in [0, 1]")
    return min(value, 0.9) if len(evidence) == 1 else value
