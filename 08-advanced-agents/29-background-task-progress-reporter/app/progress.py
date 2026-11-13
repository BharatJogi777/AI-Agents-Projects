"""Aggregate milestone progress without pretending unknown work is complete."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Milestone:
    milestone_id: str
    weight: float
    status: str

@dataclass(frozen=True)
class Progress:
    percent: float
    completed: int
    total: int
    blocked: tuple[str, ...]
    failed: tuple[str, ...]

def calculate_progress(milestones: list[Milestone]) -> Progress:
    if not milestones:
        raise ValueError("milestones cannot be empty")
    seen=set()
    total_weight=completed_weight=0.0
    blocked=[]; failed=[]; completed=0
    for m in milestones:
        if not m.milestone_id.strip() or m.milestone_id in seen:
            raise ValueError("milestone IDs must be non-empty and unique")
        seen.add(m.milestone_id)
        if m.weight <= 0:
            raise ValueError("milestone weight must be positive")
        if m.status not in {"pending","running","blocked","failed","completed"}:
            raise ValueError("unsupported milestone status")
        total_weight += m.weight
        if m.status == "completed":
            completed += 1; completed_weight += m.weight
        elif m.status == "blocked": blocked.append(m.milestone_id)
        elif m.status == "failed": failed.append(m.milestone_id)
    return Progress(round(completed_weight / total_weight * 100, 2), completed, len(milestones), tuple(blocked), tuple(failed))
