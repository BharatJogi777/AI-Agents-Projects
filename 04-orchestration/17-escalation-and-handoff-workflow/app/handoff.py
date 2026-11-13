from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Handoff:
    task_id: str
    from_owner: str
    to_owner: str
    reason: str
    level: int

class EscalationWorkflow:
    def __init__(self, levels: list[str], notify: Callable[[Handoff], Any], max_level: int | None = None):
        if not levels or any(not x.strip() for x in levels): raise ValueError("non-empty owners required")
        self.levels, self.notify = tuple(levels), notify
        self.max_level = len(levels) if max_level is None else max_level
        if not 1 <= self.max_level <= len(levels): raise ValueError("invalid max_level")
        self.history: list[Handoff] = []

    def escalate(self, task_id: str, current_level: int, reason: str) -> Handoff:
        if not task_id.strip() or not reason.strip(): raise ValueError("task and reason required")
        if not 0 <= current_level < self.max_level: raise RuntimeError("escalation limit reached")
        if current_level + 1 >= self.max_level: raise RuntimeError("no higher escalation owner configured")
        record = Handoff(task_id, self.levels[current_level], self.levels[current_level+1], reason, current_level+1)
        self.notify(record)
        self.history.append(record)
        return record
