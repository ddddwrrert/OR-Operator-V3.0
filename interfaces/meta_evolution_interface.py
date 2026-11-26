from typing import Mapping, Protocol


class StrategyEvaluator(Protocol):
    def __call__(self, engine, task: tuple, policy: Mapping, config: dict) -> dict[int, float]: ...
