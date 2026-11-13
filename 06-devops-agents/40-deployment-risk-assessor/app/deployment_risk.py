"""Explainable deployment risk scoring from a release readiness checklist."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: str
    factors: tuple[str,...]
    recommendation: str

def assess_deployment(change_size: str, *, tests_passed: bool, rollback_tested: bool, database_migration: bool=False, backward_compatible: bool=True, critical_service: bool=False, canary_available: bool=True) -> RiskAssessment:
    if change_size not in {"small","medium","large"}: raise ValueError("change_size must be small, medium, or large")
    flags=(tests_passed,rollback_tested,database_migration,backward_compatible,critical_service,canary_available)
    if any(not isinstance(x,bool) for x in flags): raise ValueError("readiness flags must be booleans")
    score={"small":5,"medium":15,"large":25}[change_size]; factors=[]
    def add(points,reason):
        nonlocal score
        score+=points; factors.append(reason)
    if not tests_passed: add(25,"Required tests have not passed.")
    if not rollback_tested: add(15,"Rollback has not been tested.")
    if database_migration: add(15,"Deployment includes a database migration.")
    if not backward_compatible: add(20,"Change is not backward compatible.")
    if critical_service: add(10,"Affected service is business critical.")
    if not canary_available: add(10,"Canary rollout is unavailable.")
    score=min(score,100); level="critical" if score>=70 else "high" if score>=50 else "medium" if score>=30 else "low"
    recommendation="Do not proceed without explicit release review and mitigation plan." if level=="critical" else "Use staged rollout, owner approval, and verified rollback." if level in {"high","medium"} else "Proceed through the normal release checklist."
    return RiskAssessment(score,level,tuple(factors),recommendation)
