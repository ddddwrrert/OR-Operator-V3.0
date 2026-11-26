def remaining(counts, limits):
    return max(0, limits["evaluations"] - counts.get("evaluations", 0))
