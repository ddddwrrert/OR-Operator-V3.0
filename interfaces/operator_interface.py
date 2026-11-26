from dataclasses import dataclass, field


@dataclass(frozen=True)
class Operator:
    name: str
    description: str
    body: str
    reads: tuple[str, ...] = ()
    writes: tuple[str, ...] = ()
    before: tuple[str, ...] = ()
    metadata: dict = field(default_factory=dict)
