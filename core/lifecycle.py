from contextlib import contextmanager
from pathlib import Path


@contextmanager
def exclusive_run(work):
    root = Path(work)
    root.mkdir(parents=True, exist_ok=True)
    lock = root / ".active-run"
    with lock.open("x", encoding="utf-8") as handle:
        import os
        handle.write(str(os.getpid()))
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)
