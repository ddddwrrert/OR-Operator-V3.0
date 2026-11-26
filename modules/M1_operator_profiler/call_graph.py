def graph(regions):
    return {region["name"]: sorted(set(region["calls"])) for region in regions}
