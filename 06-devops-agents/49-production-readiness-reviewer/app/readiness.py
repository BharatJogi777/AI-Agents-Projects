"""Score a production-readiness checklist with explicit missing controls."""
from dataclasses import dataclass

REQUIRED=("health_checks","metrics","centralized_logs","tracing","alerts","runbook","owner_assigned","rollback_tested","backup_verified","security_review")
@dataclass(frozen=True)
class ReadinessReport:
    score_percent: float
    status: str
    passed: tuple[str,...]
    missing: tuple[str,...]

def review_readiness(checks: dict[str,bool]) -> ReadinessReport:
    if not isinstance(checks,dict): raise TypeError("checks must be an object")
    unknown=set(checks)-set(REQUIRED)
    if unknown: raise ValueError(f"unknown checks: {sorted(unknown)}")
    if any(not isinstance(v,bool) for v in checks.values()): raise ValueError("all check values must be booleans")
    passed=tuple(k for k in REQUIRED if checks.get(k) is True); missing=tuple(k for k in REQUIRED if checks.get(k) is not True)
    score=round(len(passed)/len(REQUIRED)*100,1)
    status="ready_for_review" if not missing else "not_ready" if len(missing)>=4 or any(x in missing for x in ("security_review","rollback_tested","owner_assigned")) else "gaps_remaining"
    return ReadinessReport(score,status,passed,missing)
