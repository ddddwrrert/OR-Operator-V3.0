from random import Random


def choose(arms, samples, seed=0):
    rng = Random(seed)
    for arm in arms:
        if not samples.get(arm):
            return arm
    def draw(arm):
        data = samples[arm]
        positives = [max(0, min(1, value)) for value in data]
        return rng.betavariate(1 + sum(positives), 1 + len(data) - sum(positives))
    return max(arms, key=draw)
