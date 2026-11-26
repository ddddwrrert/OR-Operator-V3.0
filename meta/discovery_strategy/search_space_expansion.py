def step_size(value):
    if not isinstance(value, (int, float)) or not 0.1 <= value <= 0.7:
        raise ValueError("Search step is outside the approved envelope")
    return float(value)
