from core.evolution_controller import advance
from core.search_controller import SearchController
from evaluation.report_generator import write_report
from memory.evolution_history import history
from memory.strategy_performance import performance
from meta.composition_strategy.composition_policy import composition_fields
from modules.M2_bottleneck_diagnosis import diagnosis_strategy_manager
from modules.M3_operator_discovery import discovery_strategy_manager
from modules.M4_operator_validation import validation_strategy_manager


class MetaController(SearchController):
    def policy(self, engine, defaults):
        policy = advance(engine, defaults)
        return {**diagnosis_strategy_manager.options(policy),
                **discovery_strategy_manager.options(policy),
                **validation_strategy_manager.options(policy, engine.config),
                **composition_fields(policy),
                "composition_limit": policy["composition_limit"]}

    def publish(self, engine):
        super().publish(engine)
        state = engine.state.data
        records = history(state)
        for identifier, policy in state.get("strategies", {}).items():
            write_report(engine.workspace, "recursive_evolution", "strategy-" + identifier, policy)
        return write_report(engine.workspace, "recursive_evolution", "history", {
            "active": state.get("active_strategy"), "archive": state.get("strategies", {}),
            "trials": records, "performance": performance(records)})
