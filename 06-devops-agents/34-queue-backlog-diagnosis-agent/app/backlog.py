"""Diagnose queue backlog trends from consecutive metric windows."""
from dataclasses import dataclass

@dataclass(frozen=True)
class BacklogFinding:
    severity: str
    issue: str
    evidence: str
    next_check: str

def diagnose_backlog(snapshot: dict) -> list[BacklogFinding]:
    if not isinstance(snapshot,dict): raise TypeError("snapshot must be an object")
    keys=("backlog","previous_backlog","arrivals_per_minute","processed_per_minute","retry_count","dead_letter_count")
    values={}
    for k in keys:
        v=snapshot.get(k,0)
        if isinstance(v,bool) or not isinstance(v,(int,float)) or v<0: raise ValueError(f"{k} must be non-negative numeric")
        values[k]=v
    out=[]; net=values["arrivals_per_minute"]-values["processed_per_minute"]
    if values["backlog"]>values["previous_backlog"] and net>0:
        out.append(BacklogFinding("high","Backlog is growing",f"Arrival rate exceeds processing by {net:g}/minute","Inspect consumer concurrency, processing latency, downstream throttling, and scaling limits."))
    if values["retry_count"]>0: out.append(BacklogFinding("medium","Retries are occurring",str(values["retry_count"]),"Inspect transient failures, retry policy, exponential backoff, and poison messages."))
    if values["dead_letter_count"]>0: out.append(BacklogFinding("high","Messages reached dead-letter queue",str(values["dead_letter_count"]),"Inspect message failure reasons and use an approved replay procedure."))
    if values["backlog"]>0 and values["processed_per_minute"]==0: out.append(BacklogFinding("critical","Queue is not draining",f"{values['backlog']} messages pending","Check consumer health, permissions, queue visibility/lease settings, and dependency availability."))
    return out
