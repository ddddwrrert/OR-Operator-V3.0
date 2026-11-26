from dataclasses import asdict
from pathlib import Path
from budget import Budget, BudgetError
from core.event_manager import emit
from core.experiment_manager import publish, publish_memory
from core.state_manager import State
from core.version_manager import finalize
from evaluation.report_generator import write_report
from execution.code_workspace import candidate_path, write_candidate
from interfaces.discovery_interface import Discoverer
from interfaces.llm_interface import Model
from interfaces.solver_interface import Solver
from modules.M1_operator_profiler import build_profile
from modules.M2_bottleneck_diagnosis import diagnose
from modules.M3_operator_discovery import discover
from modules.M3_operator_discovery.candidate_manager import prepare
from modules.M3_operator_discovery.duplicate_detector import fingerprint
from modules.M4_operator_validation import validate


class Orchestrator:
    def __init__(self, workspace, config, solver: Solver, model_factory, extension=None):
        self.workspace = Path(workspace)
        self.config = config
        self.solver = solver
        self.extension = extension
        identity = [config, fingerprint(solver.baseline), solver.program]
        self.state = State(workspace, identity)
        self.budget = Budget(config["budget"], self.state.data, self.state.save)
        self.model: Model = model_factory(self.budget)
        self.discover: Discoverer = discover

    def run(self):
        work, solver, state = self.workspace, self.solver, self.state.data
        base = candidate_path(work, "000000", solver.program)
        if not base.exists():
            write_candidate(work, "000000", solver.program, solver.baseline)
        self.state.save()
        emit(work, "system", "run-started", version=self.config["version"])
        attempts = self.config["cycles"]
        if type(attempts) is not int or attempts < 0:
            raise ValueError("cycles must be a nonnegative integer")
        while self.budget.counts.get("candidates", 0) < attempts:
            parent_id = state["incumbent"]
            parent = candidate_path(work, parent_id, solver.program)
            source = parent.read_text(encoding="utf-8")
            options = {"window": 8, "confidence": self.config["confidence"], "step": 0.25}
            item = None
            record = {"accepted": False, "parent": parent_id, "stage": "profiling"}
            try:
                self.budget.reserve("candidates")
            except BudgetError as error:
                state["stop_reason"] = str(error)
                break
            record["id"] = f"{self.budget.counts['candidates']:06d}"
            try:
                if self.extension:
                    options = self.extension.policy(self, options)
                profile = build_profile(source, solver.program, state["history"])
                record["profile"] = profile
                record["stage"] = "diagnosis"
                diagnosis = diagnose(self.model, source, profile, state["history"], options)
                if diagnosis:
                    record["diagnosis"] = asdict(diagnosis)
                emit(work, "diagnosis", "diagnosed", id=record["id"], report=record.get("diagnosis"))
                if diagnosis and diagnosis.confidence >= options["confidence"]:
                    record["stage"] = "discovery"
                    plan = self.extension.plan(self, profile, options) if self.extension else None
                    record["plan"] = plan
                    operator = self.discover(self.model, source, diagnosis, profile, options, plan)
                    record["operator"] = {key: value for key, value in asdict(operator).items() if key != "body"}
                    item = prepare(work, solver, record, operator, source, state["history"])
                    emit(work, "discovery", "candidate-built", id=record["id"], operator=operator.name)
                    record["stage"] = "validation"
                    evaluation = dict(self.config["evaluation"])
                    if "seed_count" in options:
                        evaluation["seeds"] = evaluation["seeds"][:options["seed_count"]]
                    record.update(validate(solver, self.budget, parent, item, evaluation))
                    if self.extension:
                        self.extension.observe(self, record, parent, item, source, options)
                else:
                    record["error"] = "No qualifying falsifiable diagnosis"
            except BudgetError as error:
                record.update(stage="budget", accepted=False, error=str(error))
                state["stop_reason"] = str(error)
            except (ValueError, RuntimeError, OSError, SyntaxError, KeyError, TypeError) as error:
                record.update(accepted=False, error=str(error))
                emit(work, "execution", "candidate-error", id=record["id"], stage=record["stage"], error=str(error))
            finalize(work, state, record, item)
            self.budget.checkpoint()
            publish(work, record)
            emit(work, "validation", "decision", id=record["id"], accepted=record["accepted"], stage=record["stage"])
            if record["stage"] == "budget":
                break
        publish_memory(work, state["history"])
        result = {"version": self.config["version"], "incumbent": state["incumbent"],
                  "solver": str(candidate_path(work, state["incumbent"], solver.program)),
                  "attempts": self.budget.counts.get("candidates", 0),
                  "accepted": sum(row["accepted"] for row in state["history"]),
                  "budget_used": dict(self.budget.counts), "stop_reason": state.get("stop_reason", "cycle-limit")}
        compared = [row for row in state["history"] if row.get("pairs")]
        if compared:
            first_pair = compared[0]["pairs"][0]
            incumbent = next((row for row in compared if row["id"] == state["incumbent"]), None)
            result["initial_fitness"] = first_pair["control"]
            result["incumbent_fitness"] = incumbent["pairs"][0]["candidate"] if incumbent else first_pair["control"]
            result["reporting_seed"] = first_pair["seed"]
        if self.extension:
            self.extension.publish(self)
        write_report(work, "final", "result", result)
        self.budget.checkpoint()
        return result
