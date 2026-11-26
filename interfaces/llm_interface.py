from typing import Protocol


class Model(Protocol):
    def request(self, purpose: str, payload: dict) -> dict: ...
