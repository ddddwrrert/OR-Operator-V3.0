from statistics import mean
from evaluation.statistical_test import two_sided_sign_test


def contribution(pairs):
    values = [pair["gain"] for pair in pairs]
    return {"gain": mean(values), "sign_p_value": two_sided_sign_test(values),
            "attribution": "complete candidate change against its parent"}
