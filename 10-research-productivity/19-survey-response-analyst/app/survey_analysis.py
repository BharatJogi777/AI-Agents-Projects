"""Analyze structured survey responses without inferring respondent intent."""
from collections import Counter
from dataclasses import dataclass

@dataclass(frozen=True)
class QuestionSummary:
    question: str
    response_count: int
    missing_count: int
    distribution: dict[str, int]

def analyze_survey(*, responses: list[dict], questions: list[str]) -> list[QuestionSummary]:
    if not isinstance(responses, list) or not isinstance(questions, list):
        raise TypeError("responses and questions must be lists")
    if any(not isinstance(q, str) or not q.strip() for q in questions):
        raise ValueError("questions must contain non-empty strings")
    if len(set(questions)) != len(questions):
        raise ValueError("question names must be unique")
    for row in responses:
        if not isinstance(row, dict):
            raise TypeError("each response must be a dictionary")
    summaries=[]
    for question in questions:
        values=[row.get(question) for row in responses]
        answered=[str(v).strip() for v in values if v is not None and str(v).strip()]
        summaries.append(QuestionSummary(question, len(answered), len(responses)-len(answered), dict(sorted(Counter(answered).items()))))
    return summaries
