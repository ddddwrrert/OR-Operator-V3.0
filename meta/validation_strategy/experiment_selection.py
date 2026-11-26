def matched_jobs(tasks, seeds):
    return [(tuple(task), seed) for task in tasks for seed in seeds]
