def rollback(engine, incumbent):
    engine.state.data["active_strategy"] = incumbent
    engine.state.save()
