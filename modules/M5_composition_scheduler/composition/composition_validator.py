from execution.compiler import check
from .operator_compatibility import compatible


def check_variant(solver, path, sequence):
    if not compatible(sequence):
        raise ValueError("Composition violates a declared state or ordering constraint")
    return solver.check(path)
