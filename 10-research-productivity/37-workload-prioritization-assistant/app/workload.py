"""Explainable workload prioritization from user-supplied task metadata."""
from dataclasses import dataclass

@dataclass(frozen=True)
class WorkItem:
    id: str
    title: str
    urgency: int
    impact: int
    effort_hours: float
    blocking_others: bool = False

def prioritize(items: list[WorkItem]) -> list[dict]:
    if not items:
        return []
    seen = set()
    ranked = []
    for item in items:
        if not item.id.strip() or not item.title.strip():
            raise ValueError("item id and title must be non-empty")
        if item.id in seen:
            raise ValueError(f"duplicate item id: {item.id}")
        seen.add(item.id)
        if not 1 <= item.urgency <= 5 or not 1 <= item.impact <= 5:
            raise ValueError("urgency and impact must be between 1 and 5")
        if item.effort_hours <= 0:
            raise ValueError("effort_hours must be positive")
        score = item.urgency * 3 + item.impact * 2 + (3 if item.blocking_others else 0)
        reasons = [f"urgency={item.urgency}/5", f"impact={item.impact}/5"]
        if item.blocking_others:
            reasons.append("blocks other work")
        ranked.append({"item": item, "score": score, "priority_per_effort": round(score / item.effort_hours, 3), "reasons": reasons})
    return sorted(ranked, key=lambda x: (-x["score"], -x["priority_per_effort"], x["item"].id))
