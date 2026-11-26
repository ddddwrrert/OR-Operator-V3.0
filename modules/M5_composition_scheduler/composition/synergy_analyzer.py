from statistics import mean
from .conflict_detector import conflict
from .interaction_estimator import interaction


def analyze(per_seed):
    deltas = [interaction(row["control"], row["singles"], row["forward"]) for row in per_seed]
    orders = [row["forward"] - row["reverse"] for row in per_seed if row["reverse"] is not None]
    return {"interaction": mean(deltas), "order_effect": mean(orders) if orders else None,
            "conflict": any(conflict(row["singles"], row["forward"]) for row in per_seed),
            "paired": per_seed}
