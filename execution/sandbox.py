def command(argv, prefix=()):
    if not argv or any(not isinstance(item, str) or not item for item in [*prefix, *argv]):
        raise ValueError("Expected nonempty argument vectors")
    return [*prefix, *argv]


def require_isolation(prefix):
    if not prefix:
        raise ValueError("Organon task execution requires a configured sandbox_prefix")
    return tuple(prefix)
