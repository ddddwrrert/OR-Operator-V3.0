from .score_normalizer import merit


def compare(seed, control, candidate):
    return {"seed": seed, "control": control.score, "candidate": candidate.score,
            "gain": merit(candidate.score) - merit(control.score),
            "valid": control.valid and candidate.valid,
            "seconds": control.seconds + candidate.seconds,
            "control_metrics": control.metrics, "candidate_metrics": candidate.metrics}
