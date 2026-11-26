from budget import BudgetError
from budget.composition_budget import reserve_composition
from core.event_manager import emit
from evaluation.report_generator import write_report
from evaluation.scheduler_evaluator import publish_scheduler
from evaluation.synergy_evaluator import evaluate_variants
from execution.operator_pipeline import variants
from interfaces.composition_interface import Composition
from memory.composition_history import compositions
from memory.operator_graph import graph
from memory.operator_registry import registry
from modules.M5_composition_scheduler.composition.composition_controller import choose as choose_sequence
from modules.M5_composition_scheduler.scheduling.context_extractor import context
from modules.M5_composition_scheduler.scheduling.contextual_bandit import samples
from modules.M5_composition_scheduler.scheduling.exploration_controller import available
from modules.M5_composition_scheduler.scheduling.scheduler_controller import choose


class SearchController:
    def policy(self, engine, defaults):
        return defaults

    def plan(self, engine, profile, policy) -> Composition:
        history = engine.state.data["history"]
        composition = engine.config["composition"]
        config = engine.config["scheduler"]
        accepted = [row["operator"] for row in registry(history).values()
                    if (row.get("plan") or {}).get("kind") != "compose"]
        candidates = list(accepted)
        if composition["allow_failed"]:
            names = {item["name"] for item in candidates}
            for row in reversed(history):
                op = row.get("operator")
                if op and row.get("pairs") and op["name"] not in names and (row.get("plan") or {}).get("kind") != "compose":
                    candidates.append(op)
                    names.add(op["name"])
        sequence = choose_sequence(candidates, policy.get("max_sequence", composition["max_sequence"]), compositions(history))
        state = context(profile, history)
        arms = available(accepted, sequence, engine.budget)
        scores = samples(history, state, config["invalid_penalty"])
        algorithm = config["algorithm"]
        kind = choose(algorithm, arms, scores, config, len(history))
        plan = {"kind": kind, "algorithm": algorithm, "context": state, "arms": arms,
                "components": sequence if kind == "compose" else accepted[-1:] if kind == "reuse" else []}
        emit(engine.workspace, "scheduling", "action", plan=plan)
        return plan

    def observe(self, engine, record, parent, item, source, policy):
        plan = record["plan"]
        if plan["kind"] != "compose" or not record.get("pairs") or not engine.solver.supports_seeds:
            return
        try:
            seeds = engine.config["composition"]["seeds"]
            limit = policy.get("composition_limit", engine.config["budget"]["composition_trials"])
            reserve_composition(engine.budget, limit)
            inputs = variants(engine, record, parent, item, source, policy)
            record["composition"] = {"id": record["id"], "components": [x["name"] for x in plan["components"]],
                                     **evaluate_variants(engine.solver, engine.budget, inputs, seeds)}
            write_report(engine.workspace, "ablation", record["id"], record["composition"])
            emit(engine.workspace, "composition", "measured", report=record["composition"])
        except (BudgetError, RuntimeError, ValueError, OSError, SyntaxError) as error:
            record["composition_error"] = str(error)
            emit(engine.workspace, "composition", "evaluation-incomplete", error=str(error), id=record["id"])

    def publish(self, engine):
        history = engine.state.data["history"]
        schedule = publish_scheduler(engine.workspace, history, engine.config["scheduler"])
        links = graph([*history, *compositions(history)])
        write_report(engine.workspace, "composition", "operator-graph", links)
        write_report(engine.workspace, "composition", "experiments", compositions(history))
        return schedule
