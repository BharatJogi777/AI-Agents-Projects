"""Generate a timed agenda from explicitly supplied meeting topics."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AgendaItem:
    topic: str
    minutes: int
    desired_outcome: str

def generate_agenda(objective: str, topics: list[AgendaItem], meeting_minutes: int) -> list[dict]:
    if not objective.strip():
        raise ValueError("meeting objective is required")
    if meeting_minutes <= 0:
        raise ValueError("meeting_minutes must be positive")
    if not topics:
        raise ValueError("at least one agenda topic is required")
    total, agenda, cursor = 0, [], 0
    for item in topics:
        if not item.topic.strip() or not item.desired_outcome.strip() or item.minutes <= 0:
            raise ValueError("topics need a name, positive duration, and desired outcome")
        total += item.minutes
        agenda.append({"topic": item.topic, "start_minute": cursor, "end_minute": cursor + item.minutes, "desired_outcome": item.desired_outcome})
        cursor += item.minutes
    if total > meeting_minutes:
        raise ValueError(f"agenda requires {total} minutes but meeting has {meeting_minutes}")
    return agenda
