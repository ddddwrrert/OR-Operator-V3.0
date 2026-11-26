from pathlib import Path
from execution.code_integrator import integrate
from modules.M3_operator_discovery import discover
from modules.M5_composition_scheduler.composition.composition_validator import check_variant


def execute(engine, context, sequence, destination):
    source = context["source"]
    for component in sequence:
        proposal = discover(engine.model, source, context["diagnosis"], context["profile"],
                            context["policy"], {"kind": "reuse", "components": [component]})
        source = integrate(source, proposal.body)
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=False)
    path.write_text(source, encoding="utf-8")
    check_variant(engine.solver, path, sequence)
    return path
