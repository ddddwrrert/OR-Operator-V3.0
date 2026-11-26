def verifiable(claim, evidence, test):
    return bool(
        isinstance(claim, str) and claim.strip()
        and isinstance(evidence, (list, tuple)) and evidence
        and all(isinstance(item, str) and item.strip() for item in evidence)
        and isinstance(test, str) and test.strip()
    )
