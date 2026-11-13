"""Allowlist and sanitize low-risk Redis INFO diagnostics."""
from collections.abc import Mapping

_ALLOWED={"redis_version","uptime_in_seconds","connected_clients","used_memory_human","total_commands_processed","keyspace_hits","keyspace_misses"}

def sanitize_info(info: Mapping[str,object])->dict[str,str|int|float]:
    result={}
    for key in _ALLOWED:
        value=info.get(key)
        if isinstance(value,(str,int,float)) and not isinstance(value,bool):
            result[key]=value
    return result

def hit_rate(info: Mapping[str,object])->float|None:
    hits,misses=info.get("keyspace_hits"),info.get("keyspace_misses")
    if not isinstance(hits,int) or not isinstance(misses,int) or hits<0 or misses<0:
        return None
    total=hits+misses
    return None if total==0 else hits/total
