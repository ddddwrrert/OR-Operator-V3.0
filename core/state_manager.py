import json
from pathlib import Path


class State:
    def __init__(self, work, identity):
        root = Path(work) / "storage" / "checkpoints"
        root.mkdir(parents=True, exist_ok=True)
        self.path = root / "state.json"
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
            if self.data.get("identity") != identity:
                raise ValueError("Version, configuration or baseline changed. Use a new workspace.")
        else:
            self.data = {"identity": identity, "incumbent": "000000", "history": [], "budget": {}}

    def save(self):
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.data, ensure_ascii=False, indent=2, allow_nan=False, default=str),
                             encoding="utf-8")
        temporary.replace(self.path)
