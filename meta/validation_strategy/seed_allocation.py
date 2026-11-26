def seed_count(value, capacity):
    if type(value) is not int or not 1 <= value <= capacity:
        raise ValueError("Invalid validation seed allocation")
    return value
