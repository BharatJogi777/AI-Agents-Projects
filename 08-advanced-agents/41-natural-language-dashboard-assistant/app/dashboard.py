"""Translate a constrained natural-language request into a safe dashboard specification."""
from dataclasses import dataclass

ALLOWED_AGGREGATIONS={"count","sum","avg","min","max"}
@dataclass(frozen=True)
class DashboardSpec:
    metric: str
    aggregation: str
    dimension: str | None
    time_range: str | None

def build_dashboard_spec(*, metric: str, aggregation: str, dimension: str | None = None, time_range: str | None = None, allowed_fields: set[str]) -> DashboardSpec:
    if not metric or metric not in allowed_fields:
        raise ValueError("metric is not in the allowed field list")
    if aggregation not in ALLOWED_AGGREGATIONS:
        raise ValueError("unsupported aggregation")
    if dimension is not None and dimension not in allowed_fields:
        raise ValueError("dimension is not in the allowed field list")
    if time_range is not None and time_range not in {"24h","7d","30d","90d","1y"}:
        raise ValueError("unsupported time range")
    return DashboardSpec(metric,aggregation,dimension,time_range)

def render_spec(spec: DashboardSpec) -> dict[str, object]:
    return {"metric":spec.metric,"aggregation":spec.aggregation,"group_by":spec.dimension,"time_range":spec.time_range,"execution_required":True}
