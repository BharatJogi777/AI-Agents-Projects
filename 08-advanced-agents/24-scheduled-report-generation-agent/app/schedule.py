"""Evaluate UTC schedules; does not generate or deliver reports."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class ReportSchedule:
    schedule_id: str
    interval_minutes: int
    enabled: bool = True

@dataclass(frozen=True)
class DueReport:
    schedule_id: str
    scheduled_for: str
    idempotency_key: str

def due_reports(schedules: list[ReportSchedule], *, now: datetime, last_run: dict[str, datetime] | None = None) -> tuple[DueReport, ...]:
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    last_run = last_run or {}
    seen, due = set(), []
    current = now.astimezone(timezone.utc)
    for schedule in schedules:
        if not schedule.schedule_id.strip() or schedule.schedule_id in seen:
            raise ValueError("schedule IDs must be non-empty and unique")
        seen.add(schedule.schedule_id)
        if not 1 <= schedule.interval_minutes <= 525600:
            raise ValueError("interval_minutes must be between 1 and 525600")
        if not schedule.enabled:
            continue
        previous = last_run.get(schedule.schedule_id)
        if previous is None:
            due_at = current
        else:
            if previous.tzinfo is None or previous.utcoffset() is None:
                raise ValueError("last_run timestamps must be timezone-aware")
            due_at = previous.astimezone(timezone.utc) + __import__("datetime").timedelta(minutes=schedule.interval_minutes)
        if due_at <= current:
            stamp = due_at.isoformat()
            due.append(DueReport(schedule.schedule_id, stamp, f"{schedule.schedule_id}:{stamp}"))
    return tuple(due)
