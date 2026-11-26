from adapters.model import DemoModel
from budget import BudgetError
from budget.recursive_budget import reserve_probe
from core.event_manager import emit
from memory.evolution_history import history
from memory.strategy_archive import archive, identifier
from meta.budget_strategy.experiment_allocation import probe_cost
from meta.discovery_strategy.diversity_policy import deduplicate
from .evolution_stop_condition import can_evolve
from .evolution_trigger import triggered
from .strategy_analyzer import weaknesses
from .strategy_compiler import compile_strategy
from .strategy_crossover import crossover
from .strategy_generator import generate
from .strategy_mutator import mutate
from .strategy_promoter import promote
from .strategy_rollback import rollback
from .strategy_selector import choose
from .strategy_validator import validate


def evolve(engine, current, previous):
    state = engine.state.data
    config = engine.config["recursive"]
    attempt = engine.budget.counts["candidates"]
    if not triggered(attempt, config):
        return current
    if not isinstance(engine.model, DemoModel):
        emit(engine.workspace, "meta_evolution", "skipped", reason="No held-out task suite configured for this adapter")
        return current
    maximum = len(engine.config["evaluation"]["seeds"])
    required = probe_cost(len(config["tasks"]), len(config["heldout_seeds"]), config["training_attempts"] * maximum)
    if not can_evolve(engine.budget, required, config):
        return current
    reserve_probe(engine.budget)
    logs = history(state)
    row = {"attempt": attempt, "previous": previous, "accepted": False}
    try:
        patch = generate(engine.model, current, state["history"], weaknesses(state["history"]))
        proposed = compile_strategy(mutate(current, patch), engine.config)
        options = deduplicate([proposed, compile_strategy(crossover(current, proposed), engine.config)])
        challenger = next((item for item in options if identifier(item) not in state["strategies"]), None)
        if challenger is None:
            raise ValueError("Strategy already tested")
        row["challenger"] = archive(state, challenger)
        pairs, summary = validate(engine, current, challenger, config)
        row.update(pairs=pairs, summary=summary, accepted=choose(summary, config["minimum_gain"]))
        if row["accepted"]:
            promote(engine, row["challenger"], challenger)
            current = challenger
    except (BudgetError, RuntimeError, OSError, ValueError, SyntaxError) as error:
        row.update(accepted=False, error=str(error))
    if not row["accepted"]:
        rollback(engine, previous)
    logs.append(row)
    engine.state.save()
    emit(engine.workspace, "meta_evolution", "decision", **row)
    return current
