from itertools import combinations


def pairs(operators):
    return [pair for pair in combinations(operators, 2) if pair[0]["name"] != pair[1]["name"]]
