def confidence(value):
    if not isinstance(value, (int, float)) or not 0.5 <= value <= 0.95:
        raise ValueError("Invalid confidence threshold")
    return float(value)
