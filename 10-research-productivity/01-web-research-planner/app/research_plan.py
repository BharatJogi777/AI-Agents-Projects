"""Build a traceable research plan; this module does not browse or invent sources."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ResearchPlan:
    objective: str
    research_questions: tuple[str, ...]
    search_queries: tuple[str, ...]
    evidence_fields: tuple[str, ...]
    source_types: tuple[str, ...]
    requires_user_confirmation: bool = True

def build_research_plan(*, objective: str, audience: str, scope: str, max_questions: int = 5) -> ResearchPlan:
    for name, value in (("objective", objective), ("audience", audience), ("scope", scope)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-empty string")
    if not isinstance(max_questions, int) or isinstance(max_questions, bool) or not 1 <= max_questions <= 10:
        raise ValueError("max_questions must be an integer from 1 to 10")
    topic = objective.strip()
    questions = (
        f"What is the current state of {topic} within {scope.strip()}?",
        f"What evidence supports the main approaches to {topic}?",
        f"What limitations, risks, and disagreements are reported about {topic}?",
        f"What practical implications matter to {audience.strip()}?",
        f"What important evidence gaps remain about {topic}?",
    )[:max_questions]
    queries = tuple(dict.fromkeys((topic, f"{topic} evidence {scope.strip()}", f"{topic} limitations research")))
    return ResearchPlan(topic, questions, queries,
        ("claim", "source title", "author or organization", "publication date", "URL", "supporting passage", "limitations"),
        ("primary research", "official documentation", "systematic reviews", "reputable reporting"))
