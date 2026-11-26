def crossover(current, challenger):
    keys = ("seed_count", "composition_limit")
    return {**challenger, **{key: current[key] for key in keys if key in current}}
