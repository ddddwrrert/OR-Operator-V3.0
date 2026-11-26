def discovery_fields(policy):
    return {"step": policy.get("step", 0.25), "discovery_directive": policy.get("discovery_directive", "")}
