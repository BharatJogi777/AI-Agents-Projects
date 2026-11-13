"""Deterministic anomaly detection over daily service-cost exports."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CostAnomaly:
    service: str
    baseline: float
    observed: float
    increase: float
    increase_percent: float

def investigate_costs(baseline: dict[str, float], observed: dict[str, float], *, threshold_percent: float = 30.0, min_increase: float = 1.0) -> list[CostAnomaly]:
    if not isinstance(baseline, dict) or not isinstance(observed, dict):
        raise TypeError("baseline and observed must be mappings")
    if threshold_percent < 0 or min_increase < 0:
        raise ValueError("thresholds must be non-negative")
    results = []
    for service, current in observed.items():
        prior = baseline.get(service, 0.0)
        if not isinstance(service, str) or not service.strip():
            raise ValueError("service names must be non-empty strings")
        if isinstance(prior, bool) or isinstance(current, bool) or not isinstance(prior, (int, float)) or not isinstance(current, (int, float)):
            raise ValueError(f"cost values for {service} must be numeric")
        if prior < 0 or current < 0:
            raise ValueError(f"cost values for {service} must be non-negative")
        delta = float(current - prior)
        pct = (delta / prior * 100) if prior else (100.0 if current else 0.0)
        if delta >= min_increase and pct >= threshold_percent:
            results.append(CostAnomaly(service, float(prior), float(current), delta, round(pct, 2)))
    return sorted(results, key=lambda item: item.increase, reverse=True)
