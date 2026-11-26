from collections import Counter
from .scheduler_controller import choose


def compare_policies(history, config):
    from .contextual_bandit import samples
    decisions = {"UCB": Counter(), "Thompson": Counter()}
    observed = Counter()
    for i, row in enumerate(history):
        plan = row.get("plan") or {}
        if not plan:
            continue
        context, arms = plan["context"], plan["arms"]
        data = samples(history[:i], context, config["invalid_penalty"])
        for method in decisions:
            decisions[method][choose(method, arms, data, config, i)] += 1
        observed[(context, plan["kind"])] += 1
    return {"replay_action_counts": decisions,
            "observed": [{"context": context, "arm": arm, "count": count} for (context, arm), count in observed.items()]}
