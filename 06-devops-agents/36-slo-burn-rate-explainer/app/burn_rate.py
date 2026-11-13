"""Explain SLO error-budget burn rate from windowed request counts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class BurnRate:
    window: str
    observed_error_ratio: float
    burn_rate: float
    severity: str
    explanation: str

def explain_burn_rate(windows: list[dict], *, target_slo: float=0.999, fast_threshold: float=14.4, slow_threshold: float=6.0) -> list[BurnRate]:
    if not 0 < target_slo < 1: raise ValueError("target_slo must be between 0 and 1")
    if fast_threshold <= 0 or slow_threshold <= 0: raise ValueError("burn thresholds must be positive")
    if not isinstance(windows,list): raise TypeError("windows must be a list")
    out=[]; seen=set(); budget=1-target_slo
    for i,w in enumerate(windows):
        if not isinstance(w,dict): raise ValueError(f"window {i} must be an object")
        name=w.get("name"); total=w.get("total_requests"); errors=w.get("error_requests")
        if not isinstance(name,str) or not name.strip() or name in seen: raise ValueError(f"window {i} requires unique name")
        seen.add(name)
        if any(isinstance(v,bool) or not isinstance(v,int) for v in (total,errors)) or total<=0 or errors<0 or errors>total: raise ValueError(f"window {name} has invalid request counts")
        ratio=errors/total; burn=ratio/budget
        severity="critical" if burn>=fast_threshold else "high" if burn>=slow_threshold else "normal"
        explanation=("Rapid budget consumption; page and investigate correlated changes." if severity=="critical" else "Sustained budget consumption; investigate before budget is exhausted." if severity=="high" else "Burn rate is below configured alert thresholds.")
        out.append(BurnRate(name,ratio,round(burn,3),severity,explanation))
    return out
