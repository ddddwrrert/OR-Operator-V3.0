from memory.strategy_archive import archive
from modules.M6_recursive_evolution.recursive_controller import evolve
from modules.M6_recursive_evolution.strategy_compiler import compile_strategy


def advance(engine, defaults):
    state = engine.state.data
    identifier = state.get("active_strategy")
    if identifier is None:
        initial = compile_strategy(defaults, engine.config)
        identifier = archive(state, initial)
        state["active_strategy"] = identifier
        engine.state.save()
    policy = state["strategies"][identifier]
    return evolve(engine, policy, identifier)
