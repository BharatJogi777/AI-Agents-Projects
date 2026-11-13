"""Pure prompt-template rendering and validation."""
from dataclasses import dataclass

_ALLOWED_AUDIENCES = {"beginner", "intermediate", "expert"}


class PromptInputError(ValueError):
    """Raised when prompt arguments do not satisfy the public contract."""


@dataclass(frozen=True, slots=True)
class TechnicalBriefRequest:
    topic: str
    audience: str = "intermediate"
    include_examples: bool = True


def render_technical_brief(request: TechnicalBriefRequest) -> str:
    topic = request.topic.strip()
    audience = request.audience.strip().lower()

    if not 3 <= len(topic) <= 120:
        raise PromptInputError("topic must contain between 3 and 120 characters")
    if audience not in _ALLOWED_AUDIENCES:
        raise PromptInputError(
            "audience must be one of: beginner, intermediate, expert"
        )

    examples = (
        "Include at least two concrete examples."
        if request.include_examples
        else "Do not include examples; prioritize a concise conceptual explanation."
    )
    return (
        f"Prepare a technical brief about: {topic}\n"
        f"Target audience: {audience}.\n"
        "Define important terms, explain the underlying mechanism, and state "
        "relevant trade-offs. Separate established facts from assumptions.\n"
        f"{examples}\n"
        "Finish with a short summary and three questions a reader can use "
        "to check their understanding."
    )
