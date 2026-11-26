def composition_limit(value, maximum):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError("Composition limit exceeds its hard cap")
    return value
