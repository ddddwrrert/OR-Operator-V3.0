from statistics import mean


def summarize(pairs):
    changes = [row["challenger"] - row["control"] for row in pairs]
    return {"mean_gain": mean(changes), "positive_fraction": sum(delta > 0 for delta in changes) / len(changes),
            "worst_gain": min(changes)}
