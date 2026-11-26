def diagnoses(history):
    return [dict(id=row["id"], **row["diagnosis"]) for row in history if row.get("diagnosis")]
