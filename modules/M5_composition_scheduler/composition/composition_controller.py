from .operator_sequence_generator import sequences


def choose(operators, maximum, previous):
    options = sequences(operators, maximum)
    if not options:
        return []
    def rank(sequence):
        names = [item["name"] for item in sequence]
        visits = sum(row.get("components") == names for row in previous)
        return (visits, -len(sequence))
    return list(min(options, key=rank))
