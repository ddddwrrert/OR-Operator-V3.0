def diversity(history):
    hashes = [item["hash"] for item in history if item.get("hash")]
    return {"observations": len(hashes), "unique": len(set(hashes)),
            "source_diversity": len(set(hashes)) / len(hashes) if hashes else None}
