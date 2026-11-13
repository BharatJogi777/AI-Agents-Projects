"""Detect changes in aggregate model quality metrics."""
from dataclasses import dataclass
from math import isfinite
from typing import Mapping

@dataclass(frozen=True)
class MetricDrift:
    name: str
    baseline: float
    current: float
    delta: float
    drifted: bool

def compare_metrics(baseline: Mapping[str, float], current: Mapping[str, float], *, thresholds: Mapping[str, float]) -> tuple[MetricDrift, ...]:
    """Thresholds are absolute allowed changes; caller defines metric direction."""
    if set(baseline) != set(current):
        raise ValueError("baseline and current metrics must have identical keys")
    if set(baseline) != set(thresholds):
        raise ValueError("each metric requires a threshold")
    results = []
    for name in sorted(baseline):
        base, now, limit = baseline[name], current[name], thresholds[name]
        if not all(isinstance(x, (int, float)) and isfinite(x) for x in (base, now, limit)) or limit < 0:
            raise ValueError("metrics must be finite numbers and thresholds non-negative")
        delta = float(now) - float(base)
        results.append(MetricDrift(name, float(base), float(now), delta, abs(delta) > limit))
    return tuple(results)
