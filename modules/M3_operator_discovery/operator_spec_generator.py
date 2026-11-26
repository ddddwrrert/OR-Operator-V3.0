from interfaces.operator_interface import Operator


def specification(idea, code):
    def fields(key):
        value = idea.get(key, [])
        if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"Operator {key} must be a string array")
        return tuple(value)

    def label(key):
        value = idea[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing operator {key}")
        return value.strip()

    return Operator(label("name"), label("rationale"), code, fields("reads"),
                    fields("writes"), fields("before"), idea.get("metadata", {}))
