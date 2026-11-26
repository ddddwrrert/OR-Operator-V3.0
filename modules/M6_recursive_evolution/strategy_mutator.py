def mutate(previous, patch):
    if not isinstance(patch, dict):
        raise ValueError("Strategy patch must be a mapping")
    return {**previous, **patch}
