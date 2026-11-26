from .reward_calculator import reward


def samples(history, context, penalty):
    result = {}
    for item in history:
        plan = item.get("plan") or {}
        if plan.get("context") == context:
            result.setdefault(plan["kind"], []).append(reward(item, penalty))
    return result
