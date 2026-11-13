"""Rank PostgreSQL performance observations without executing SQL or changing settings."""
from dataclasses import dataclass

@dataclass(frozen=True)
class PerformanceFinding:
    priority: str
    signal: str
    evidence: str
    investigation: str

def analyze_snapshot(snapshot: dict) -> list[PerformanceFinding]:
    if not isinstance(snapshot,dict): raise TypeError("snapshot must be an object")
    findings=[]
    for key in ("deadlocks","blocked_queries","long_transactions","cache_hit_ratio","replication_lag_seconds","unused_indexes"):
        if key in snapshot and (isinstance(snapshot[key],bool) or not isinstance(snapshot[key],(int,float)) or snapshot[key]<0):
            raise ValueError(f"{key} must be a non-negative number")
    if snapshot.get("deadlocks",0)>0: findings.append(PerformanceFinding("critical","Deadlocks",str(snapshot["deadlocks"]),"Inspect deadlock logs, transaction ordering, and lock scope."))
    if snapshot.get("blocked_queries",0)>0: findings.append(PerformanceFinding("high","Blocked queries",str(snapshot["blocked_queries"]),"Inspect pg_stat_activity, lock chains, and long-running transactions."))
    if snapshot.get("long_transactions",0)>0: findings.append(PerformanceFinding("high","Long transactions",str(snapshot["long_transactions"]),"Identify idle-in-transaction sessions and transaction boundaries."))
    if "cache_hit_ratio" in snapshot and snapshot["cache_hit_ratio"]<0.90: findings.append(PerformanceFinding("medium","Low cache hit ratio",str(snapshot["cache_hit_ratio"]),"Review workload, working-set size, indexes, and buffer/cache configuration."))
    if snapshot.get("replication_lag_seconds",0)>30: findings.append(PerformanceFinding("high","Replication lag",str(snapshot["replication_lag_seconds"]),"Inspect replica load, WAL generation, network throughput, and replication slot retention."))
    if snapshot.get("unused_indexes",0)>0: findings.append(PerformanceFinding("low","Potentially unused indexes",str(snapshot["unused_indexes"]),"Validate over a representative period before considering index removal."))
    return findings
