"""Analyze Kafka consumer group lag snapshots without connecting to a cluster."""
from dataclasses import dataclass

@dataclass(frozen=True)
class LagFinding:
    group: str
    topic: str
    partition: int
    lag: int
    severity: str
    explanation: str

def investigate_lag(records: list[dict], *, warning_lag: int=1000, critical_lag: int=10000) -> list[LagFinding]:
    if not isinstance(records,list): raise TypeError("records must be a list")
    if warning_lag<0 or critical_lag<warning_lag: raise ValueError("invalid lag thresholds")
    out=[]; seen=set()
    for i,r in enumerate(records):
        if not isinstance(r,dict): raise ValueError(f"record {i} must be an object")
        group,topic,part,lag=r.get("group"),r.get("topic"),r.get("partition"),r.get("lag")
        if not isinstance(group,str) or not group or not isinstance(topic,str) or not topic: raise ValueError(f"record {i} requires group and topic")
        if isinstance(part,bool) or not isinstance(part,int) or part<0 or isinstance(lag,bool) or not isinstance(lag,int) or lag<0: raise ValueError(f"record {i} has invalid partition or lag")
        key=(group,topic,part)
        if key in seen: raise ValueError(f"duplicate partition record: {key}")
        seen.add(key)
        if lag>=critical_lag: sev="critical"
        elif lag>=warning_lag: sev="high"
        else: continue
        out.append(LagFinding(group,topic,part,lag,sev,"Consumer offset is materially behind the log end; inspect throughput, errors, and partition assignment."))
    return sorted(out,key=lambda x:x.lag,reverse=True)
