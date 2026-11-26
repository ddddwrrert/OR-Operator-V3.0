from modules.M5_composition_scheduler.composition.operator_sequence_generator import sequences


def eligible(operators, maximum):
    return [list(order) for order in sequences(operators, maximum)]
