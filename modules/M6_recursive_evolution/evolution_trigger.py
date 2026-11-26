def triggered(attempt, config):
    first = config["trigger_after"]
    return attempt >= first and (attempt - first) % config["interval"] == 0
