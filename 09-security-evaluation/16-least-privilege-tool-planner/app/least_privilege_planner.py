"""Select the smallest authorized tool set for declared task capabilities."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Tool:
    name: str
    capabilities: frozenset[str]
    risk: int = 1

@dataclass(frozen=True)
class Plan:
    selected: tuple[str, ...]
    missing: tuple[str, ...]
    total_risk: int

def plan_tools(required: set[str], tools: list[Tool], *, max_risk: int = 5) -> Plan:
    if not isinstance(required, set) or any(not isinstance(x, str) or not x.strip() for x in required):
        raise ValueError("required must be a set of non-empty capability strings")
    if max_risk < 0:
        raise ValueError("max_risk must be non-negative")
    if len({t.name for t in tools}) != len(tools):
        raise ValueError("tool names must be unique")
    if any(t.risk < 0 for t in tools):
        raise ValueError("tool risk must be non-negative")
    uncovered = set(required)
    selected = []
    remaining = list(tools)
    while uncovered:
        candidates = [t for t in remaining if t.capabilities & uncovered and sum(x.risk for x in selected) + t.risk <= max_risk]
        if not candidates:
            break
        best = min(candidates, key=lambda t: (-len(t.capabilities & uncovered), t.risk, t.name))
        selected.append(best)
        uncovered -= best.capabilities
        remaining.remove(best)
    return Plan(tuple(t.name for t in selected), tuple(sorted(uncovered)), sum(t.risk for t in selected))
