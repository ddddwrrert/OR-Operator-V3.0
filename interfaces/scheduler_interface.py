from typing import Protocol


class Scheduler(Protocol):
    def __call__(self, arms: list[str], samples: dict[str, list[float]]) -> str: ...
