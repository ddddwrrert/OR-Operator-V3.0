from typing import TypedDict


class Composition(TypedDict):
    kind: str
    components: list[dict]
    context: str
    algorithm: str
    arms: list[str]
