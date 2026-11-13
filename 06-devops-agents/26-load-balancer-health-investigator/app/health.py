"""Classify load-balancer target health from exported target status records."""
from dataclasses import dataclass

@dataclass(frozen=True)
class TargetFinding:
    target_id: str
    severity: str
    reason: str
    recommendation: str

REASONS = {
    "Target.Timeout": ("high", "Health check timed out; inspect target reachability, port, and response latency."),
    "Target.ResponseCodeMismatch": ("medium", "Health check response did not match configured success codes."),
    "Target.FailedHealthChecks": ("high", "Repeated health checks failed; inspect application health and dependencies."),
    "Target.NotInUse": ("low", "Target is not currently registered for an active listener path."),
    "Elb.InternalError": ("high", "Load balancer reported an internal health-check error; correlate service events."),
}

def investigate_targets(targets: list[dict]) -> list[TargetFinding]:
    if not isinstance(targets, list): raise TypeError("targets must be a list")
    out=[]; seen=set()
    for i,t in enumerate(targets):
        if not isinstance(t,dict): raise ValueError(f"target {i} must be an object")
        tid=t.get("id"); state=t.get("state"); reason=t.get("reason","")
        if not isinstance(tid,str) or not tid.strip() or tid in seen: raise ValueError(f"target {i} requires a unique non-empty id")
        seen.add(tid)
        if state not in {"healthy","unhealthy","initial","draining","unused"}: raise ValueError(f"target {tid}: invalid state")
        if state=="healthy": continue
        severity,advice=REASONS.get(reason,("medium","Inspect target health details, listener configuration, and application logs."))
        if state in {"initial","draining","unused"} and reason not in REASONS: severity="low"
        out.append(TargetFinding(tid,severity,reason or f"Target state is {state}",advice))
    return out
