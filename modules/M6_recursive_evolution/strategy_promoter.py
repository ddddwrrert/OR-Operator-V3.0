from execution.checkpoint_manager import checkpoint


def promote(engine, identifier, policy):
    checkpoint(engine.workspace, identifier, policy)
    engine.state.data["active_strategy"] = identifier
    engine.state.save()
