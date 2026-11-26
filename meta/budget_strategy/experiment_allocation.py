def probe_cost(task_count, seed_count, training_count):
    return 2 * task_count * (seed_count + 2 * training_count)
