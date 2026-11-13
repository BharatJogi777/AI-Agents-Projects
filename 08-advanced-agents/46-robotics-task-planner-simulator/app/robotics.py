"""Plan grid-based robot movements with obstacle and bounds validation."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Position:
    x: int
    y: int

def plan_path(start: Position, goals: Iterable[Position], *, width: int, height: int, obstacles: set[Position]) -> list[Position]:
    if width<=0 or height<=0:
        raise ValueError("grid dimensions must be positive")
    def valid(p: Position) -> bool:
        return 0<=p.x<width and 0<=p.y<height and p not in obstacles
    if not valid(start):
        raise ValueError("start is outside the grid or blocked")
    current=start
    route=[start]
    for goal in goals:
        if not valid(goal):
            raise ValueError("goal is outside the grid or blocked")
        # Deterministic Manhattan route: horizontal, then vertical.
        while current.x!=goal.x:
            current=Position(current.x+(1 if goal.x>current.x else -1),current.y)
            if not valid(current): raise ValueError(f"route blocked at {current}")
            route.append(current)
        while current.y!=goal.y:
            current=Position(current.x,current.y+(1 if goal.y>current.y else -1))
            if not valid(current): raise ValueError(f"route blocked at {current}")
            route.append(current)
    return route
