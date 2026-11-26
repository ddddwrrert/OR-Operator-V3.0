def directive(value):
    if not isinstance(value, str) or len(value) > 600:
        raise ValueError("Invalid strategy directive")
    return value
