from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Outcome:
    score: float
    seconds: float
    valid: bool
    metrics: dict = field(default_factory=dict)


class Evaluator(Protocol):
    def evaluate(self, source: Path, seed: int) -> Outcome: ...
