from .operator_classifier import classify
from .state_transition_analyzer import transitions


def extract(regions):
    return [{"location": region["name"], "kind": classify(region), **transitions(region)}
            for region in regions if region["writes"] or region["branches"] or region["calls"]]
