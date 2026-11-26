def reward(record, penalty=0.2):
    if not record.get("accepted"):
        return -penalty
    efficiency = record["gain"] / max(record["seconds"], 0.001)
    return min(1.0, efficiency)
