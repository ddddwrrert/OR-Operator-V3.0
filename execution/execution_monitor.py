from dataclasses import dataclass


@dataclass(frozen=True)
class Execution:
    returncode: int
    stdout: str
    stderr: str
    seconds: float

    def require_success(self):
        if self.returncode:
            raise RuntimeError(self.stderr[-2000:] or f"Process exited {self.returncode}")
        return self
