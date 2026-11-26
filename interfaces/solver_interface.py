from pathlib import Path
from typing import Protocol
from interfaces.evaluator_interface import Outcome


class Solver(Protocol):
    program: str
    baseline: str
    supports_seeds: bool

    def check(self, source: Path) -> None: ...
    def evaluate(self, source: Path, seed: int) -> Outcome: ...
