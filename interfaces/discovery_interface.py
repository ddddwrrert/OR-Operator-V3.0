from typing import Protocol
from interfaces.diagnosis_interface import Diagnosis
from interfaces.llm_interface import Model
from interfaces.operator_interface import Operator


class Discoverer(Protocol):
    def __call__(self, model: Model, source: str, diagnosis: Diagnosis, profile: dict,
                 policy: dict, plan: dict | None) -> Operator: ...
