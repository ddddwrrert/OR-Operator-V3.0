from evaluation.report_generator import write_report


def checkpoint(work, policy_id, policy):
    return write_report(work, "recursive_evolution", "checkpoint-" + policy_id, policy)
