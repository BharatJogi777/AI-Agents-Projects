"""Refine vague research prompts into bounded, answerable questions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RefinedQuestion:
    primary_question: str
    subquestions: tuple[str, ...]
    assumptions: tuple[str, ...]
    missing_dimensions: tuple[str, ...]

def refine_question(*, topic: str, audience: str, timeframe: str = "", geography: str = "",
                    desired_evidence: str = "") -> RefinedQuestion:
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be non-empty")
    dimensions = {"audience": audience, "timeframe": timeframe, "geography": geography, "desired evidence": desired_evidence}
    if any(not isinstance(v, str) for v in dimensions.values()):
        raise ValueError("all dimensions must be strings")
    missing = tuple(name for name, value in dimensions.items() if not value.strip())
    parts = [topic.strip()]
    if audience.strip(): parts.append(f"for {audience.strip()}")
    if geography.strip(): parts.append(f"in {geography.strip()}")
    if timeframe.strip(): parts.append(f"during {timeframe.strip()}")
    primary = "What does the available evidence show about " + " ".join(parts) + "?"
    subs = (
        f"What are the main approaches and how do they compare for {topic.strip()}?",
        f"What measurable outcomes and trade-offs are reported for {topic.strip()}?",
        f"What limitations, risks, and unresolved questions remain?",
    )
    assumptions = ("The question is exploratory, not a request to confirm a predetermined conclusion.",)
    return RefinedQuestion(primary, subs, assumptions, missing)
