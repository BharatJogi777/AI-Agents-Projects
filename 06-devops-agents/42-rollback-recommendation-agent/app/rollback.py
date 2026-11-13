"""Decision support for rollback; never executes a rollback."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RollbackAdvice:
    action: str
    reasons: tuple[str,...]
    requires_human_approval: bool=True

def recommend_rollback(*, error_rate: float, baseline_error_rate: float, latency_p95_ms: float, baseline_latency_p95_ms: float, impact_minutes: int, rollback_tested: bool, data_compatible: bool, customer_impact: bool=False) -> RollbackAdvice:
    for name,v in (("error_rate",error_rate),("baseline_error_rate",baseline_error_rate)):
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not 0<=v<=1: raise ValueError(f"{name} must be in [0,1]")
    for name,v in (("latency_p95_ms",latency_p95_ms),("baseline_latency_p95_ms",baseline_latency_p95_ms)):
        if isinstance(v,bool) or not isinstance(v,(int,float)) or v<0: raise ValueError(f"{name} must be non-negative")
    if isinstance(impact_minutes,bool) or not isinstance(impact_minutes,int) or impact_minutes<0: raise ValueError("impact_minutes must be non-negative")
    if any(not isinstance(v,bool) for v in (rollback_tested,data_compatible,customer_impact)): raise ValueError("readiness and impact flags must be booleans")
    reasons=[]
    if error_rate>max(baseline_error_rate*2,baseline_error_rate+0.01): reasons.append("Error rate is materially above baseline.")
    if latency_p95_ms>max(baseline_latency_p95_ms*1.5,baseline_latency_p95_ms+100): reasons.append("P95 latency is materially above baseline.")
    if impact_minutes>=5: reasons.append("Impact has persisted for at least five minutes.")
    if customer_impact: reasons.append("Customer impact is reported.")
    if not reasons: return RollbackAdvice("continue_monitoring",("No configured regression trigger was detected.",))
    if not rollback_tested or not data_compatible: return RollbackAdvice("hold_and_escalate",tuple(reasons+["Rollback readiness or data compatibility is not confirmed; assess a safe mitigation with the owner."]))
    return RollbackAdvice("consider_rollback_with_approval",tuple(reasons+["Rollback appears technically prepared but requires incident-owner approval."]))
