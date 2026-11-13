"""Deterministic aggregation of structured multi-agent results."""
from dataclasses import dataclass
from statistics import mean
from typing import Any

@dataclass(frozen=True)
class AgentResult:
    agent_id: str
    value: Any
    confidence: float
    errors: tuple[str, ...] = ()

@dataclass(frozen=True)
class Aggregate:
    values: tuple[AgentResult, ...]
    accepted: tuple[AgentResult, ...]
    rejected: tuple[AgentResult, ...]
    average_confidence: float

def aggregate(results: list[AgentResult], minimum_confidence: float = 0.0,
              require_unique_agents: bool = True) -> Aggregate:
    if not 0 <= minimum_confidence <= 1:
        raise ValueError("minimum_confidence must be in [0, 1]")
    if any(not r.agent_id or not 0 <= r.confidence <= 1 for r in results):
        raise ValueError("each result needs an agent ID and confidence in [0, 1]")
    if require_unique_agents and len({r.agent_id for r in results}) != len(results):
        raise ValueError("duplicate agent result")
    accepted = tuple(r for r in results if r.confidence >= minimum_confidence and not r.errors)
    rejected = tuple(r for r in results if r not in accepted)
    avg = mean(r.confidence for r in accepted) if accepted else 0.0
    return Aggregate(tuple(results), accepted, rejected, avg)
