"""Deterministic sealed-bid task auction."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Bid:
    agent_id: str
    price: float
    estimated_seconds: float
    capabilities: frozenset[str]

@dataclass(frozen=True)
class Award:
    task_id: str
    agent_id: str
    price: float
    score: float

def award_task(task_id: str, required: set[str], bids: list[Bid],
               budget: float, max_seconds: float) -> Award:
    if not task_id or budget < 0 or max_seconds <= 0:
        raise ValueError("invalid task or auction constraints")
    if len({b.agent_id for b in bids}) != len(bids):
        raise ValueError("one bid per agent is allowed")
    eligible = [b for b in bids if b.price >= 0 and b.price <= budget
                and 0 < b.estimated_seconds <= max_seconds
                and required <= b.capabilities]
    if not eligible:
        raise RuntimeError("no eligible bids")
    winner = min(eligible, key=lambda b: (b.price, b.estimated_seconds, b.agent_id))
    return Award(task_id, winner.agent_id, winner.price,
                 winner.price / budget if budget else 0.0)
