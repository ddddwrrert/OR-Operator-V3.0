def robustness(pairs):
    gains = [pair["gain"] for pair in pairs]
    return {"minimum": min(gains), "positive_fraction": sum(x > 0 for x in gains) / len(gains)}
