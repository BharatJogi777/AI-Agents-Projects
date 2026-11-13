"""Compare canary metrics against a baseline without changing traffic."""
from dataclasses import dataclass

@dataclass(frozen=True)
class MetricResult:
    name: str
    baseline: float
    canary: float
    relative_change_percent: float
    status: str

@dataclass(frozen=True)
class CanaryReport:
    decision: str
    metrics: tuple[MetricResult,...]
    reasons: tuple[str,...]

def analyze_canary(baseline: dict, canary: dict, *, tolerances: dict | None=None, min_samples: int=100) -> CanaryReport:
    if not isinstance(baseline,dict) or not isinstance(canary,dict) or set(baseline)!=set(canary) or not baseline: raise ValueError("baseline and canary must contain the same non-empty metric names")
    if isinstance(min_samples,bool) or not isinstance(min_samples,int) or min_samples<1: raise ValueError("min_samples must be positive")
    tolerances=tolerances or {}; results=[]; reasons=[]
    for name in sorted(baseline):
        b=baseline[name]; c=canary[name]
        if not isinstance(name,str) or not name: raise ValueError("metric names must be non-empty strings")
        for label,v in (("baseline",b),("canary",c)):
            if not isinstance(v,dict): raise ValueError(f"{label}.{name} must be an object")
            value=v.get("value"); count=v.get("samples")
            if isinstance(value,bool) or not isinstance(value,(int,float)) or value<0: raise ValueError(f"{label}.{name}.value must be non-negative")
            if isinstance(count,bool) or not isinstance(count,int) or count<0: raise ValueError(f"{label}.{name}.samples must be a non-negative integer")
        tolerance=tolerances.get(name,10.0)
        if isinstance(tolerance,bool) or not isinstance(tolerance,(int,float)) or not 0<=tolerance<=1000: raise ValueError(f"invalid tolerance for {name}")
        bv,cv=float(b["value"]),float(c["value"]); change=0.0 if bv==0 and cv==0 else (float("inf") if bv==0 else (cv-bv)/bv*100)
        if b["samples"]<min_samples or c["samples"]<min_samples: status="insufficient_data"; reasons.append(f"{name}: sample count below minimum")
        elif change>tolerance: status="regression"; reasons.append(f"{name}: regression exceeds {tolerance}% tolerance")
        else: status="within_tolerance"
        results.append(MetricResult(name,bv,cv,change,status))
    decision="hold_for_more_data" if any(x.status=="insufficient_data" for x in results) else "investigate_regression" if any(x.status=="regression" for x in results) else "canary_looks_healthy"
    return CanaryReport(decision,tuple(results),tuple(reasons))
