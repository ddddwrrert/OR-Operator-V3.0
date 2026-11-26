import argparse
import json
from pathlib import Path
from adapters.baseline_adapter import Baseline
from adapters.model import CompatibleModel, DemoModel
from adapters.organon_adapter import OrganonAdapter
from config import load
from core.lifecycle import exclusive_run
from core.meta_controller import MetaController
from core.orchestrator import Orchestrator


def main(argv=None):
    parser = argparse.ArgumentParser(description="OR-Operator independent search runner")
    parser.add_argument("--work", type=Path, default=Path("python-demo"))
    parser.add_argument("--config", type=Path)
    parser.add_argument("--organon", type=Path)
    parser.add_argument("--task", type=Path)
    args = parser.parse_args(argv)
    config = load(args.config)
    work = args.work.resolve()
    if bool(args.organon) != bool(args.task):
        parser.error("--organon and --task must be supplied together")
    if args.organon and (work == args.organon.resolve() or work.is_relative_to(args.organon.resolve())):
        parser.error("The working directory must be outside original Organon")
    if args.task and (work == args.task.resolve() or work.is_relative_to(args.task.resolve())):
        parser.error("The working directory must be outside the task directory")
    with exclusive_run(work):
        if args.organon:
            solver = OrganonAdapter(args.organon, args.task, work, config["solver"])
            def model_factory(budget):
                return CompatibleModel(config["llm"], budget)
        else:
            solver = Baseline(config["demo_targets"], config["solver"]["timeout"])
            def model_factory(_budget):
                return DemoModel(solver.target)
        result = Orchestrator(work, config, solver, model_factory, MetaController()).run()
    print(json.dumps(result, ensure_ascii=False))
    return result


def cli():
    main()


if __name__ == "__main__":
    cli()
