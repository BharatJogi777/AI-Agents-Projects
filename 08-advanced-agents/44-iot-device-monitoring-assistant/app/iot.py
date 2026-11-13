"""Evaluate IoT telemetry against explicit thresholds and report stale devices."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class Reading:
    device_id: str
    metric: str
    value: float
    observed_at: datetime

@dataclass(frozen=True)
class Finding:
    device_id: str
    metric: str
    severity: str
    message: str

def inspect_readings(readings: list[Reading], *, thresholds: dict[str,tuple[float,float]], now: datetime, stale_after_seconds: int = 300) -> list[Finding]:
    if now.tzinfo is None or stale_after_seconds < 0:
        raise ValueError("now must be timezone-aware and stale_after_seconds non-negative")
    findings=[]
    for r in readings:
        if not r.device_id or r.metric not in thresholds:
            raise ValueError("device id and configured metric threshold are required")
        if r.observed_at.tzinfo is None:
            raise ValueError("reading timestamp must be timezone-aware")
        low,high=thresholds[r.metric]
        if low>high:
            raise ValueError("threshold lower bound exceeds upper bound")
        age=(now.astimezone(timezone.utc)-r.observed_at.astimezone(timezone.utc)).total_seconds()
        if age>stale_after_seconds:
            findings.append(Finding(r.device_id,r.metric,"warning",f"Reading is stale by {int(age)} seconds"))
        if r.value<low or r.value>high:
            findings.append(Finding(r.device_id,r.metric,"critical",f"Value {r.value} outside [{low}, {high}]"))
    return findings
