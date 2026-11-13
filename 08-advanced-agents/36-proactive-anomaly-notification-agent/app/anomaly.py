"""Detect unusual metric values and create deduplicated notification candidates."""
from dataclasses import dataclass
from statistics import median
from typing import Iterable

@dataclass(frozen=True)
class Metric:
    name: str
    value: float
    observed_at: str

@dataclass(frozen=True)
class Alert:
    metric: str
    value: float
    baseline: float
    deviation: float
    observed_at: str
    dedupe_key: str

def detect_anomalies(metrics: Iterable[Metric], *, threshold: float = 3.0, min_history: int = 3) -> list[Alert]:
    """Compare each point with the median of earlier points; no external notification is sent."""
    if threshold <= 0 or min_history < 2:
        raise ValueError("threshold must be positive and min_history at least 2")
    history: dict[str, list[float]] = {}
    alerts = []
    for item in metrics:
        if not item.name.strip() or not item.observed_at.strip():
            raise ValueError("metric name and timestamp are required")
        if not isinstance(item.value, (int, float)):
            raise TypeError("metric value must be numeric")
        prior = history.setdefault(item.name, [])
        if len(prior) >= min_history:
            baseline = float(median(prior))
            deviations = [abs(v - baseline) for v in prior]
            scale = float(median(deviations)) * 1.4826
            if scale == 0:
                scale = max(abs(baseline) * 0.01, 1e-9)
            score = abs(float(item.value) - baseline) / scale
            if score >= threshold:
                key = f"{item.name}:{item.observed_at}"
                alerts.append(Alert(item.name, float(item.value), baseline, score, item.observed_at, key))
        prior.append(float(item.value))
    return alerts

def notification_candidates(alerts: Iterable[Alert], already_sent: Iterable[str] = ()) -> list[Alert]:
    """Return unsent candidates only; caller must apply its own approval/delivery policy."""
    sent = set(already_sent)
    return [a for a in alerts if a.dedupe_key not in sent]
