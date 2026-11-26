from pathlib import Path


def candidate_path(work, identifier, program):
    if Path(program).name != program or not identifier.isdecimal():
        raise ValueError("Invalid candidate path")
    return Path(work) / "storage" / "candidates" / identifier / program


def write_candidate(work, identifier, program, source):
    path = candidate_path(work, identifier, program)
    path.parent.mkdir(parents=True, exist_ok=False)
    path.write_text(source, encoding="utf-8")
    return path
