def decisions(history):
    return [{"id": row["id"], **row["plan"], "accepted": row["accepted"]}
            for row in history if row.get("plan")]
