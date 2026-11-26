from .diagnosis_memory import diagnoses
from .experiment_history import experiments
from .failure_memory import failures
from .operator_history import operator_history
from .operator_registry import registry


def index(history):
    return {"diagnoses": diagnoses(history), "experiments": experiments(history),
            "failures": failures(history), "operators": operator_history(history),
            "registry": registry(history)}
