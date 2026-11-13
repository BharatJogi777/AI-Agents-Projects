"""Explainable topic coverage metric for answer evaluation."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class RelevanceReport:
    score: float
    covered_topics: tuple[str, ...]
    missing_topics: tuple[str, ...]

def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))

def evaluate_relevance(answer: str, required_topics: list[str]) -> RelevanceReport:
    if not isinstance(answer, str) or not answer.strip(): raise ValueError("answer must be non-empty")
    if not required_topics or any(not isinstance(t, str) or not t.strip() for t in required_topics):
        raise ValueError("required_topics must contain non-empty strings")
    answer_tokens=_tokens(answer)
    covered=[]; missing=[]
    for topic in required_topics:
        topic_tokens=_tokens(topic)
        if topic_tokens and topic_tokens.issubset(answer_tokens): covered.append(topic)
        else: missing.append(topic)
    return RelevanceReport(len(covered)/len(required_topics),tuple(covered),tuple(missing))
