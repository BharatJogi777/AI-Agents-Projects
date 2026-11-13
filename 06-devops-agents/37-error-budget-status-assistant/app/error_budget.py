"""Calculate remaining error budget using explicit period request counts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class BudgetStatus:
    allowed_errors: float
    observed_errors: int
    remaining_errors: float
    consumed_percent: float
    status: str

def calculate_budget(total_requests: int, observed_errors: int, *, target_slo: float=0.999, warning_percent: float=50.0, critical_percent: float=90.0) -> BudgetStatus:
    if isinstance(total_requests,bool) or not isinstance(total_requests,int) or total_requests<=0: raise ValueError("total_requests must be a positive integer")
    if isinstance(observed_errors,bool) or not isinstance(observed_errors,int) or observed_errors<0 or observed_errors>total_requests: raise ValueError("observed_errors must be between zero and total_requests")
    if not 0<target_slo<1: raise ValueError("target_slo must be between 0 and 1")
    if not 0<=warning_percent<critical_percent<=100: raise ValueError("thresholds must satisfy 0 <= warning < critical <= 100")
    allowed=total_requests*(1-target_slo); consumed=observed_errors/allowed*100 if allowed else 100.0
    remaining=allowed-observed_errors
    status="exhausted" if remaining<=0 else "critical" if consumed>=critical_percent else "warning" if consumed>=warning_percent else "healthy"
    return BudgetStatus(allowed,observed_errors,remaining,round(consumed,2),status)
