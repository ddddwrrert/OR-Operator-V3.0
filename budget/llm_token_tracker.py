import json


def estimate_input(payload):
    return len(json.dumps(payload, ensure_ascii=True).encode("utf-8"))


def reserve_for_call(payload, output_limit):
    return estimate_input(payload) + output_limit
