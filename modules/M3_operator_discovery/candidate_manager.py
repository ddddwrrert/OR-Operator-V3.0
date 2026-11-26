from execution.code_workspace import write_candidate
from .duplicate_detector import duplicate, fingerprint
from .interface_adapter_generator import adapt


def prepare(work, solver, record, operator, source, history):
    proposal = adapt(source, operator)
    if duplicate(proposal, source, history, record["parent"]):
        raise ValueError("Duplicate candidate")
    record["hash"] = fingerprint(proposal)
    return write_candidate(work, record["id"], solver.program, proposal)
