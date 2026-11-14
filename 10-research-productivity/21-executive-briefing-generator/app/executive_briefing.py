"""Build an evidence-labelled executive briefing from supplied information."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Briefing:
    headline: str
    key_updates: tuple[str, ...]
    metrics: tuple[str, ...]
    risks: tuple[str, ...]
    decisions_needed: tuple[str, ...]
    source_labels: tuple[str, ...]

def build_briefing(*, headline: str, updates: list[str], metrics: list[str], risks: list[str], decisions_needed: list[str], source_labels: list[str]) -> Briefing:
    """Normalize supplied content; never invent missing business context."""
    if not isinstance(headline, str) or not headline.strip():
        raise ValueError("headline must be non-empty")
    groups = {"updates": updates, "metrics": metrics, "risks": risks, "decisions_needed": decisions_needed, "source_labels": source_labels}
    for name, values in groups.items():
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(f"{name} must be a list of non-empty strings")
    return Briefing(headline.strip(), tuple(v.strip() for v in updates), tuple(v.strip() for v in metrics), tuple(v.strip() for v in risks), tuple(v.strip() for v in decisions_needed), tuple(v.strip() for v in source_labels))
