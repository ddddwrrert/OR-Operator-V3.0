from evaluation.report_generator import write_report
from memory.memory_index import index


def publish(work, record):
    if record.get("diagnosis"):
        write_report(work, "diagnosis", record["id"], record["diagnosis"])
    if record.get("pairs"):
        write_report(work, "operator_comparison", record["id"], record)
    write_report(work, "experiment", record["id"], record)


def publish_memory(work, history):
    return write_report(work, "final", "memory", index(history))
