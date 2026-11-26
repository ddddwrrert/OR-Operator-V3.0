def trajectory(history, window):
    recent = history[-window:]
    return {
        "recent": [{"id": item["id"], "gain": item.get("gain", 0),
                    "accepted": bool(item.get("accepted"))} for item in recent],
        "stagnation": next((i for i, row in enumerate(reversed(history)) if row.get("accepted")), len(history)),
    }
