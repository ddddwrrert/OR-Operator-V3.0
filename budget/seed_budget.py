def allocate(seeds, count=None):
    result = tuple(seeds)
    if len(set(result)) != len(result) or not result or not all(type(i) is int for i in result):
        raise ValueError("Seed list must contain unique integers")
    return result if count is None else result[:count]
