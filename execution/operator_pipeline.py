from interfaces.diagnosis_interface import Diagnosis
from execution.sequence_executor import execute
from modules.M5_composition_scheduler.composition.operator_compatibility import compatible


def variants(engine, record, parent, candidate, source, policy):
    components = record["plan"]["components"]
    context = {"source": source, "diagnosis": Diagnosis(**record["diagnosis"]),
               "profile": record["profile"], "policy": policy}
    folder = engine.workspace / "storage" / "compositions" / record["id"]
    paths = {"control": parent, "forward": candidate}
    for i, item in enumerate(components):
        paths[f"single-{i}"] = execute(engine, context, [item], folder / f"single-{i}" / candidate.name)
    reverse = components[::-1]
    paths["reverse"] = execute(engine, context, reverse, folder / "reverse" / candidate.name) if compatible(reverse) else None
    return paths
