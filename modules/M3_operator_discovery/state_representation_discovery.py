def state_space(profile):
    return sorted({state for operator in profile["operators"] for state in operator["writes"]})
