from dataclasses import asdict
from .operator_code_generator import code_for
from .operator_design_reasoner import select
from .operator_idea_generator import ideas
from .operator_spec_generator import specification
from .state_representation_discovery import state_space


def discover(model, source, diagnosis, profile, policy, plan):
    context = {"source": source, "diagnosis": asdict(diagnosis), "state": state_space(profile),
               "directive": policy.get("discovery_directive", ""), "step": policy.get("step", 0.25), "plan": plan}
    idea = select(ideas(model, context))
    return specification(idea, code_for(model, idea, context))
