def allows(limits, counts, key, amount):
    if key not in limits or type(amount) is not int or amount < 0:
        raise ValueError("Invalid budget reservation")
    return counts.get(key, 0) + amount <= limits[key]
