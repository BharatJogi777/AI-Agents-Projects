from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Checkpoint:
    completed: tuple[str, ...]
    outputs: dict[str, Any]
    next_step: int

class CheckpointedWorkflow:
    def __init__(self, steps: list[tuple[str, Callable[[dict[str, Any]], Any]]]):
        if not steps or len({name for name, _ in steps}) != len(steps):
            raise ValueError("steps must be non-empty and uniquely named")
        self.steps = tuple(steps)

    def run(self, state: dict[str, Any] | None = None, checkpoint: Checkpoint | None = None) -> Checkpoint:
        outputs = dict(checkpoint.outputs if checkpoint else (state or {}))
        completed = list(checkpoint.completed if checkpoint else ())
        start = checkpoint.next_step if checkpoint else 0
        if not 0 <= start <= len(self.steps): raise ValueError("invalid checkpoint position")
        if tuple(name for name, _ in self.steps[:start]) != tuple(completed):
            raise ValueError("checkpoint does not match workflow")
        for index in range(start, len(self.steps)):
            name, handler = self.steps[index]
            outputs[name] = handler(dict(outputs))
            completed.append(name)
        return Checkpoint(tuple(completed), outputs, len(self.steps))
