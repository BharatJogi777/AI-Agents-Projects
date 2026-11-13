"""Diagnose database connection symptoms from a normalized metrics snapshot."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ConnectionFinding:
    severity: str
    issue: str
    evidence: str
    next_check: str

def investigate_connections(snapshot: dict) -> list[ConnectionFinding]:
    if not isinstance(snapshot,dict): raise TypeError("snapshot must be an object")
    findings=[]
    for key in ("active","max_connections","waiting","timeouts","refused","auth_failures"):
        value=snapshot.get(key,0)
        if isinstance(value,bool) or not isinstance(value,int) or value<0: raise ValueError(f"{key} must be a non-negative integer")
    active=snapshot.get("active",0); maximum=snapshot.get("max_connections",0)
    if maximum and active>maximum: raise ValueError("active connections cannot exceed max_connections")
    if maximum and active/maximum>=0.9: findings.append(ConnectionFinding("high","Connection capacity near exhaustion",f"{active}/{maximum} connections active","Inspect pool sizing, leaked connections, query duration, and database connection limits."))
    if snapshot.get("waiting",0)>0: findings.append(ConnectionFinding("high","Clients waiting for connections",f"{snapshot['waiting']} waiting clients","Check pool queueing, transaction duration, and saturation across application instances."))
    if snapshot.get("timeouts",0)>0: findings.append(ConnectionFinding("medium","Connection timeouts observed",f"{snapshot['timeouts']} timeouts","Correlate network latency, DNS, database load, and connect timeout configuration."))
    if snapshot.get("refused",0)>0: findings.append(ConnectionFinding("high","Connection attempts refused",f"{snapshot['refused']} refused attempts","Verify listener availability, firewall rules, endpoint, and database restart events."))
    if snapshot.get("auth_failures",0)>0: findings.append(ConnectionFinding("high","Authentication failures observed",f"{snapshot['auth_failures']} failures","Check secret rotation, username, grants, and authentication policy; do not log credentials."))
    return findings
