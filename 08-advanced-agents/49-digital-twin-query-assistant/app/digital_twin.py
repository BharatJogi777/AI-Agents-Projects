"""Answer digital-twin queries only from supplied, timestamped asset telemetry."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

@dataclass(frozen=True)
class Observation:
    asset_id: str
    metric: str
    value: float
    unit: str
    observed_at: datetime

def query_observations(observations: Iterable[Observation], *, asset_id: str, metric: str, as_of: datetime) -> list[Observation]:
    if not asset_id.strip() or not metric.strip() or as_of.tzinfo is None:
        raise ValueError("asset, metric and timezone-aware as_of are required")
    cutoff=as_of.astimezone(timezone.utc)
    matches=[]
    for item in observations:
        if item.observed_at.tzinfo is None:
            raise ValueError("observation timestamps must be timezone-aware")
        if item.asset_id==asset_id and item.metric==metric and item.observed_at.astimezone(timezone.utc)<=cutoff:
            matches.append(item)
    return sorted(matches,key=lambda x:x.observed_at)

def summarize(observations: Iterable[Observation]) -> dict[str,object]:
    items=list(observations)
    if not items:
        return {"count":0,"latest":None,"min":None,"max":None,"average":None}
    values=[float(x.value) for x in items]
    return {"count":len(items),"latest":items[-1],"min":min(values),"max":max(values),"average":sum(values)/len(values)}
