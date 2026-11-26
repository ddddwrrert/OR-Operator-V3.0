import json
from pathlib import Path
from datetime import datetime, timezone

TOPICS = {"system", "diagnosis", "discovery", "validation", "execution",
          "composition", "scheduling", "meta_evolution"}


def emit(work, topic, event, **details):
    if topic not in TOPICS:
        raise ValueError(f"Unknown log topic: {topic}")
    path = Path(work) / "logs" / topic / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    item = {"at": datetime.now(timezone.utc).isoformat(), "event": event, **details}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, ensure_ascii=False, allow_nan=False, default=str) + "\n")
