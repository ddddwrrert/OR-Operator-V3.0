def promote(summary, threshold):
    return summary["mean_gain"] > threshold and summary["positive_fraction"] > 0.5 and summary["worst_gain"] >= -threshold
