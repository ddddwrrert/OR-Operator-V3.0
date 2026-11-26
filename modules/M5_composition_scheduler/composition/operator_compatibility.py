def compatible(sequence):
    names = [item["name"] for item in sequence]
    if len(names) != len(set(names)):
        return False
    for i, first in enumerate(sequence):
        if set(first.get("before", ())) & set(names[:i]):
            return False
        for second in sequence[i + 1:]:
            shared = set(first.get("writes", ())) & set(second.get("writes", ()))
            if shared and second["name"] not in first.get("before", ()):
                return False
    return True
