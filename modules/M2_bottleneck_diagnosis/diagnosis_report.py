from interfaces.diagnosis_interface import Diagnosis
from .bottleneck_hypothesis_generator import generate
from .confidence_estimator import estimate
from .evidence_collector import collect
from .hypothesis_verifier import verifiable


def diagnose(model, source, profile, history, policy):
    evidence = collect(profile, history, policy.get("window", 8))
    raw = generate(model, evidence, source, policy.get("diagnosis_directive", ""))
    claim, observations, test = (raw.get(key) for key in ("claim", "evidence", "test"))
    if not verifiable(claim, observations, test):
        return None
    return Diagnosis(claim, tuple(observations), test, estimate(raw.get("confidence", 0), observations))
