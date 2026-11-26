def compositions(history):
    return [row["composition"] for row in history if row.get("composition")]
