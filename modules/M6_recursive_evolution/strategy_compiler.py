from meta.budget_strategy.budget_policy import composition_limit
from meta.composition_strategy.sequence_policy import length
from meta.diagnosis_strategy.evidence_selection import window
from meta.diagnosis_strategy.hypothesis_policy import confidence
from meta.discovery_strategy.operator_generation_policy import directive
from meta.discovery_strategy.search_space_expansion import step_size
from meta.validation_strategy.seed_allocation import seed_count

ALLOWED = {"window", "confidence", "step", "max_sequence", "composition_limit", "seed_count",
           "discovery_directive", "diagnosis_directive"}


def compile_strategy(policy, config):
    if set(policy) - ALLOWED:
        raise ValueError("Unsupported policy fields")
    return {
        "window": window(policy.get("window", 8)),
        "confidence": confidence(policy.get("confidence", config["confidence"])),
        "step": step_size(policy.get("step", 0.25)),
        "max_sequence": length(policy.get("max_sequence", config["composition"]["max_sequence"])),
        "composition_limit": composition_limit(policy.get("composition_limit", config["budget"]["composition_trials"]),
                                               config["budget"]["composition_trials"]),
        "seed_count": seed_count(policy.get("seed_count", len(config["evaluation"]["seeds"])),
                                 len(config["evaluation"]["seeds"])),
        "discovery_directive": directive(policy.get("discovery_directive", "")),
        "diagnosis_directive": directive(policy.get("diagnosis_directive", "")),
    }
