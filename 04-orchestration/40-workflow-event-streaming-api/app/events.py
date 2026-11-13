"""In-memory ordered workflow event stream with replay cursors."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class WorkflowEvent:
    sequence: int
    workflow_id: str
    event_type: str
    payload: dict[str, Any]
    created_at: datetime

class EventStream:
    def __init__(self):
        self._events: dict[str, list[WorkflowEvent]] = {}

    def publish(self, workflow_id: str, event_type: str, payload: dict[str, Any]) -> WorkflowEvent:
        if not workflow_id or not event_type or not isinstance(payload, dict):
            raise ValueError("workflow_id, event_type and dictionary payload are required")
        stream = self._events.setdefault(workflow_id, [])
        event = WorkflowEvent(len(stream) + 1, workflow_id, event_type,
                              dict(payload), datetime.now(timezone.utc))
        stream.append(event)
        return event

    def replay(self, workflow_id: str, after_sequence: int = 0,
               limit: int = 100) -> tuple[WorkflowEvent, ...]:
        if after_sequence < 0 or limit < 1:
            raise ValueError("cursor must be non-negative and limit positive")
        return tuple(self._events.get(workflow_id, [])[after_sequence:after_sequence + limit])

    def latest_sequence(self, workflow_id: str) -> int:
        return len(self._events.get(workflow_id, []))
