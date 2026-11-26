def classify(region):
    if "assert" in region["branches"]:
        return "constraint"
    if region["writes"] and set(region["branches"]) & {"for", "while"}:
        return "iterative-state-update"
    if region["writes"]:
        return "state-update"
    return "read-or-evaluate"
