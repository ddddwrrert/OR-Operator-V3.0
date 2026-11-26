def current_incumbent(current, record):
    return record["id"] if record.get("accepted") else current
