from pathlib import Path
from shutil import copyfile
from modules.M4_operator_validation.rollback_manager import current_incumbent


def finalize(work, state, record, candidate):
    status = "accepted" if record.get("accepted") else "rejected"
    folder = Path(work) / "storage" / status / record["id"]
    folder.mkdir(parents=True, exist_ok=True)
    if candidate is not None and candidate.is_file():
        copyfile(candidate, folder / candidate.name)
    state["incumbent"] = current_incumbent(state["incumbent"], record)
    state["history"].append(record)
