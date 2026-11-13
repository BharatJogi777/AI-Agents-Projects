"""Capability-covering dynamic team composition."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Agent:
    agent_id: str
    capabilities: frozenset[str]
    cost: float = 1.0
    available: bool = True

@dataclass(frozen=True)
class Team:
    members: tuple[Agent, ...]
    covered_capabilities: frozenset[str]
    total_cost: float

def compose_team(agents: list[Agent], required: set[str], min_size: int = 1,
                 max_size: int = 5) -> Team:
    if min_size < 1 or max_size < min_size:
        raise ValueError("invalid team size bounds")
    if any(a.cost < 0 for a in agents):
        raise ValueError("agent cost cannot be negative")
    if len({a.agent_id for a in agents}) != len(agents):
        raise ValueError("agent IDs must be unique")
    pool = [a for a in agents if a.available]
    if len(pool) < min_size:
        raise RuntimeError("not enough available agents")
    selected: list[Agent] = []
    covered: set[str] = set()
    while not required <= covered and len(selected) < max_size:
        candidates = [a for a in pool if a not in selected]
        if not candidates:
            break
        def score(agent: Agent):
            gain = len((agent.capabilities & required) - covered)
            return (-(gain / (agent.cost + 1.0)), -gain, agent.cost, agent.agent_id)
        best = min(candidates, key=score)
        if not ((best.capabilities & required) - covered):
            break
        selected.append(best)
        covered.update(best.capabilities)
    if not required <= covered:
        raise RuntimeError("available agents cannot cover required capabilities within max_size")
    remaining = sorted((a for a in pool if a not in selected), key=lambda a: (a.cost, a.agent_id))
    while len(selected) < min_size:
        if not remaining:
            raise RuntimeError("cannot satisfy minimum team size")
        selected.append(remaining.pop(0))
    members = tuple(sorted(selected, key=lambda a: a.agent_id))
    return Team(members, frozenset(covered), sum(a.cost for a in members))
