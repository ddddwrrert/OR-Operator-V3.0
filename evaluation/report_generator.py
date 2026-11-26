import json
from pathlib import Path


def write_report(work, category, name, data):
    folder = Path(work) / "reports" / category
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (name + ".json")
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False, default=str), encoding="utf-8")
    temp.replace(path)
    return path
