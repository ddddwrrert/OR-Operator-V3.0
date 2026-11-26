from evaluation.runtime_evaluator import total_seconds


def cost_benefit(pairs, gain):
    seconds = total_seconds(pairs)
    return {"seconds": seconds, "gain_per_second": gain / max(seconds, 1e-9)}
