def transitions(region):
    return {"writes": sorted(set(region["writes"])), "guards": sorted(set(region["branches"]))}
