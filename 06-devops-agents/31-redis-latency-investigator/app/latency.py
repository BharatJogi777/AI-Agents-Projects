"""Analyze Redis latency and resource metrics from a read-only snapshot."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Finding:
    severity: str
    signal: str
    evidence: str
    next_check: str

def investigate_redis(snapshot: dict, *, latency_warning_ms: float=10.0) -> list[Finding]:
    if not isinstance(snapshot,dict): raise TypeError("snapshot must be an object")
    if latency_warning_ms<0: raise ValueError("latency_warning_ms must be non-negative")
    findings=[]
    for key in ("p95_latency_ms","p99_latency_ms","evictions","used_memory_bytes","max_memory_bytes","connected_clients","blocked_clients","slow_commands"):
        v=snapshot.get(key,0)
        if isinstance(v,bool) or not isinstance(v,(int,float)) or v<0: raise ValueError(f"{key} must be non-negative numeric")
    p95=snapshot.get("p95_latency_ms",0); p99=snapshot.get("p99_latency_ms",0)
    if p99<p95: raise ValueError("p99 latency cannot be lower than p95")
    if p95>latency_warning_ms: findings.append(Finding("high","Elevated p95 latency",f"{p95} ms","Inspect slowlog, command mix, network RTT, and CPU saturation."))
    if p99>latency_warning_ms*2: findings.append(Finding("critical","Severe tail latency",f"{p99} ms","Correlate slow commands, big keys, fork activity, and noisy neighbors."))
    if snapshot.get("evictions",0)>0: findings.append(Finding("high","Key evictions",str(snapshot["evictions"]),"Review maxmemory policy, working-set size, and TTL strategy."))
    maximum=snapshot.get("max_memory_bytes",0); used=snapshot.get("used_memory_bytes",0)
    if maximum and used/maximum>=0.9: findings.append(Finding("high","Memory near configured limit",f"{used}/{maximum} bytes","Review memory growth, fragmentation, and capacity headroom."))
    if snapshot.get("blocked_clients",0)>0: findings.append(Finding("medium","Blocked clients",str(snapshot["blocked_clients"]),"Inspect blocking commands and client timeout behavior."))
    if snapshot.get("slow_commands",0)>0: findings.append(Finding("medium","Slow commands recorded",str(snapshot["slow_commands"]),"Review Redis slowlog and command-level latency distribution."))
    return findings
