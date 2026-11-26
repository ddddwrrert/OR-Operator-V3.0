def experiments(history):
    return [row for row in history if row.get("pairs")]
