def performance(history):
    return [{"previous": row["previous"], "challenger": row["challenger"],
             "accepted": row["accepted"], "mean_gain": row["summary"]["mean_gain"]}
            for row in history if "summary" in row]
