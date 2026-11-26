def length(value):
    if type(value) is not int or value not in {2, 3}:
        raise ValueError("Invalid composition sequence length")
    return value
