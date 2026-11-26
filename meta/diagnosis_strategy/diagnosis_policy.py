def diagnosis_fields(policy):
    return {"window": policy.get("window", 8), "confidence": policy.get("confidence", 0.55),
            "diagnosis_directive": policy.get("diagnosis_directive", "")}
