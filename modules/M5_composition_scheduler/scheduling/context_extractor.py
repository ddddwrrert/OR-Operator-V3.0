def context(profile, history):
    recent = history[-3:]
    plateau = len(recent) == 3 and not any(item.get("accepted") for item in recent)
    state_size = len({entry for item in profile["operators"] for entry in item["writes"]})
    return ("plateau" if plateau else "exploration") + ":" + ("compact" if state_size < 8 else "wide")
