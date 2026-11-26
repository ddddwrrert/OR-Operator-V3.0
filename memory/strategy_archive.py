import json
from hashlib import sha256


def identifier(policy):
    data = json.dumps(policy, ensure_ascii=False, sort_keys=True)
    return sha256(data.encode()).hexdigest()[:16]


def archive(state, policy):
    value = identifier(policy)
    state.setdefault("strategies", {})[value] = policy
    return value
