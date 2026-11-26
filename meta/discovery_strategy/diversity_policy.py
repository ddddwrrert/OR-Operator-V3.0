def deduplicate(policies):
    seen = set()
    for item in policies:
        key = tuple(sorted(item.items()))
        if key not in seen:
            seen.add(key)
            yield item
