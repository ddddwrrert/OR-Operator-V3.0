from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnosis:
    claim: str
    evidence: tuple[str, ...]
    test: str
    confidence: float
