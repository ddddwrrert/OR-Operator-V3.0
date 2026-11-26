from collections import Counter


def weaknesses(history):
    return dict(Counter(row.get("stage", "unknown") for row in history[-12:] if not row["accepted"]))
