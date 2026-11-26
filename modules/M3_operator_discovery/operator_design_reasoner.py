def select(ideas):
    feasible = [idea for idea in ideas if isinstance(idea, dict)
                and str(idea.get("rationale", "")).strip() and str(idea.get("name", "")).strip()]
    if not feasible:
        raise ValueError("No reasoned operator design")
    return feasible[0]
