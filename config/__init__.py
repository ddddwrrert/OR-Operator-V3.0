from pathlib import Path
import yaml


def load(path=None):
    folder = Path(__file__).resolve().parent
    result = {}
    for item in sorted(folder.glob("*.yaml")):
        data = yaml.safe_load(item.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Expected mapping in {item}")
        result.update(data)
    if path:
        override = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        if not isinstance(override, dict):
            raise ValueError("Override must be a mapping")
        for key, value in override.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = {**result[key], **value}
            else:
                result[key] = value
    return result
