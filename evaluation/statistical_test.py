from math import comb


def two_sided_sign_test(deltas):
    plus, minus = sum(x > 0 for x in deltas), sum(x < 0 for x in deltas)
    total = plus + minus
    return min(1.0, 2 * sum(comb(total, i) for i in range(min(plus, minus) + 1)) / (2 ** total))
