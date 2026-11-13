"""Evaluate agent trajectories for completion, budget, and invalid transitions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class TrajectoryReport:
    steps: int
    completed: bool
    within_step_budget: bool
    invalid_transitions: tuple[int,...]
    score: float

def evaluate_trajectory(states: list[str], *, terminal_states: set[str], allowed_transitions: set[tuple[str,str]], max_steps: int) -> TrajectoryReport:
    if not isinstance(max_steps,int) or isinstance(max_steps,bool) or max_steps < 0: raise ValueError("max_steps must be a non-negative integer")
    if any(not isinstance(s,str) or not s for s in states) or any(not isinstance(s,str) or not s for s in terminal_states):
        raise ValueError("states must be non-empty strings")
    invalid=tuple(i for i,(a,b) in enumerate(zip(states,states[1:])) if (a,b) not in allowed_transitions)
    completed=bool(states) and states[-1] in terminal_states
    within=len(states)<=max_steps
    score=(1.0 if completed else 0.0) * (1.0 if within else 0.0) * (1.0 if not invalid else 0.0)
    return TrajectoryReport(len(states),completed,within,invalid,score)
