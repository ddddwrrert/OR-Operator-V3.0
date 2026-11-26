def window(value):
    if type(value) is not int or not 2 <= value <= 24:
        raise ValueError("Invalid diagnosis evidence window")
    return value
