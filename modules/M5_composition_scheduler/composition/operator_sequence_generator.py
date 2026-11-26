from itertools import permutations
from .operator_compatibility import compatible
from .operator_pair_generator import pairs


def sequences(operators, maximum):
    if maximum not in {2, 3}:
        raise ValueError("Sequence limit must be 2 or 3")
    pool = operators[:6]
    proposals = [perm for pair in pairs(pool) for perm in permutations(pair)]
    if maximum >= 3:
        proposals.extend(permutations(pool, 3))
    return [sequence for sequence in proposals if compatible(sequence)]
