import ast
from pathlib import Path
from tempfile import TemporaryDirectory
from execution.code_integrator import executable
from execution.process_runner import run


def check(path, *, compiler="g++", timeout=10, prefix=()):
    source = executable(path.read_text(encoding="utf-8"))
    if path.suffix == ".py":
        ast.parse(source, filename=str(path))
        compile(source, str(path), "exec")
        return
    if path.suffix not in {".cpp", ".cc", ".cxx"}:
        raise ValueError(f"Unsupported solver type {path.suffix}")
    with TemporaryDirectory(dir=path.parent) as temporary:
        clean = Path(temporary) / path.name
        clean.write_text(source, encoding="utf-8")
        run([compiler, "-std=c++17", "-fsyntax-only", str(clean)], cwd=temporary,
            timeout=timeout, prefix=prefix).require_success()
