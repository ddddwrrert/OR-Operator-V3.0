import os
import subprocess
import time
from execution.execution_monitor import Execution
from execution.sandbox import command


def run(argv, *, cwd, timeout, prefix=(), env=None):
    started = time.monotonic()
    try:
        result = subprocess.run(command(argv, prefix), cwd=cwd, env={**os.environ, **(env or {})},
                                capture_output=True, text=True, encoding="utf-8", errors="replace",
                                timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        raise TimeoutError(f"Process exceeded {timeout}s") from error
    return Execution(result.returncode, result.stdout, result.stderr, time.monotonic() - started)
