"""Portable agent handoff packets with explicit state and constraints."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Handoff:
    session_id: str
    objective: str
    completed: tuple[str, ...]
    pending: tuple[str, ...]
    constraints: tuple[str, ...]

def create_handoff(*, session_id: str, objective: str, completed: list[str], pending: list[str], constraints: list[str]) -> Handoff:
    if not session_id.strip() or not objective.strip():
        raise ValueError("session_id and objective are required")
    if not pending and not completed:
        raise ValueError("handoff must include completed or pending work")
    for group in (completed, pending, constraints):
        if any(not item.strip() for item in group):
            raise ValueError("handoff entries cannot be empty")
    if set(completed) & set(pending):
        raise ValueError("work cannot be both completed and pending")
    return Handoff(session_id, objective, tuple(completed), tuple(pending), tuple(constraints))
