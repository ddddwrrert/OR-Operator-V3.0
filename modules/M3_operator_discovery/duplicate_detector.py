from hashlib import sha256


def fingerprint(source):
    return sha256(source.encode("utf-8")).hexdigest()


def duplicate(source, parent, history, parent_id):
    hash_id = fingerprint(source)
    return source == parent or any(item.get("parent") == parent_id and item.get("hash") == hash_id
                                   for item in history if item.get("stage") != "budget")
