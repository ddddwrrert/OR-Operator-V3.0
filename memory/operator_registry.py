def registry(history):
    accepted = {}
    for row in history:
        if row.get("accepted") and row.get("operator"):
            accepted[row["operator"]["name"]] = row
    return accepted
