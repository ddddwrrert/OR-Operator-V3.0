from execution.code_integrator import split


def check_scope(before, after):
    original = split(before)
    proposed = split(after)
    if original[::2] != proposed[::2] or original[1] == proposed[1]:
        raise ValueError("Candidate must change only the EVOLVE body")
