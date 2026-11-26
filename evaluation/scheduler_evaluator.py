from evaluation.report_generator import write_report
from memory.scheduling_history import decisions
from modules.M5_composition_scheduler.scheduling.scheduler_evaluator import compare_policies


def publish_scheduler(work, history, config):
    report = compare_policies(history, config)
    report["decisions"] = decisions(history)
    return write_report(work, "scheduling", "policy-replay", report)
