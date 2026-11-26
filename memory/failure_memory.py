def failures(history):
    return [{key: item[key] for key in ("id", "stage", "error") if key in item}
            for item in history if not item.get("accepted")]
