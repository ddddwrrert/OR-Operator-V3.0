from .operator_performance_analyzer import rank
from .search_trace_analyzer import trajectory
from .state_diversity_analyzer import diversity


def collect(profile, history, window):
    return {"profile": profile, "trajectory": trajectory(history, window),
            "diversity": diversity(history[-window:]), "performance": rank(profile)}
