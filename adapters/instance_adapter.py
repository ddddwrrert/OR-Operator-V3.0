import math


def instances(target, seed, size=13):
    return [([math.sin((i + 1) * (j + 2) + seed) for j in range(len(target))])
            for i in range(size)]


def expected(row, target):
    return sum(x * y for x, y in zip(row, target, strict=True))
