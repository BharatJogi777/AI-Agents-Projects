"""Deadline tracking with injectable clock for deterministic tests."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from collections.abc import Callable

@dataclass(frozen=True)
class Deadline:
    workflow_id: str
    due_at: datetime

class DeadlineManager:
    def __init__(self, clock: Callable[[], datetime] | None = None):
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._deadlines: dict[str, Deadline] = {}

    def schedule(self, workflow_id: str, timeout: timedelta) -> Deadline:
        if not workflow_id or timeout.total_seconds() <= 0:
            raise ValueError("workflow_id and positive timeout are required")
        now = self._clock()
        if now.tzinfo is None:
            raise ValueError("clock must return timezone-aware datetime")
        deadline = Deadline(workflow_id, now + timeout)
        self._deadlines[workflow_id] = deadline
        return deadline

    def cancel(self, workflow_id: str) -> bool:
        return self._deadlines.pop(workflow_id, None) is not None

    def expired(self) -> tuple[Deadline, ...]:
        now = self._clock()
        if now.tzinfo is None:
            raise ValueError("clock must return timezone-aware datetime")
        return tuple(sorted((d for d in self._deadlines.values() if d.due_at <= now),
                            key=lambda d: (d.due_at, d.workflow_id)))

    def remaining(self, workflow_id: str) -> timedelta:
        deadline = self._deadlines[workflow_id]
        return max(timedelta(0), deadline.due_at - self._clock())
