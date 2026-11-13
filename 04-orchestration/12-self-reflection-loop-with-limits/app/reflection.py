from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class ReflectionResult:
    output: Any
    attempts: int
    accepted: bool
    feedback: str

class ReflectionLoop:
    def __init__(self, execute: Callable[[str, str], Any], evaluate: Callable[[Any], tuple[bool, str]], max_attempts: int = 3):
        if max_attempts < 1: raise ValueError("max_attempts must be positive")
        self.execute, self.evaluate, self.max_attempts = execute, evaluate, max_attempts

    def run(self, task: str) -> ReflectionResult:
        if not task.strip(): raise ValueError("task is required")
        feedback, output = "", None
        for attempt in range(1, self.max_attempts + 1):
            output = self.execute(task, feedback)
            accepted, next_feedback = self.evaluate(output)
            if not isinstance(accepted, bool) or not isinstance(next_feedback, str):
                raise TypeError("evaluator must return (bool, str)")
            feedback = next_feedback
            if accepted: return ReflectionResult(output, attempt, True, feedback)
        return ReflectionResult(output, self.max_attempts, False, feedback)
