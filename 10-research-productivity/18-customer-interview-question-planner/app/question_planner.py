"""Plan neutral customer interview questions from explicit objectives."""
from dataclasses import dataclass

@dataclass(frozen=True)
class InterviewQuestion:
    objective: str
    question: str
    follow_up: str

def plan_questions(*, objectives: list[str]) -> list[InterviewQuestion]:
    if not isinstance(objectives, list):
        raise TypeError("objectives must be a list")
    result = []
    for objective in objectives:
        if not isinstance(objective, str) or not objective.strip():
            raise ValueError("every objective must be a non-empty string")
        clean = objective.strip().rstrip("?.")
        result.append(InterviewQuestion(
            objective=clean,
            question=f"Can you walk me through your experience with {clean.lower()}?",
            follow_up="What happened next, and what made that difficult or easy?",
        ))
    return result
