def summarize(history):
    stats = {}
    for item in history:
        name = item.get("operator", {}).get("name")
        if not name:
            continue
        values = stats.setdefault(name, {"attempts": 0, "accepted": 0, "seconds": 0, "gain": 0})
        values["attempts"] += 1
        values["accepted"] += bool(item.get("accepted"))
        values["seconds"] += item.get("seconds", 0)
        values["gain"] += item.get("gain", 0)
    return stats


def telemetry(history):
    measured = {}
    for candidate in history:
        for pair in candidate.get("pairs", []):
            operators = pair.get("candidate_metrics", {}).get("operators", {})
            if not isinstance(operators, dict):
                continue
            for name, sample in operators.items():
                if not isinstance(sample, dict):
                    continue
                row = measured.setdefault(name, {"calls": 0, "seconds": 0})
                for key in row:
                    value = sample.get(key)
                    if isinstance(value, (int, float)) and value >= 0:
                        row[key] += value
    return measured
