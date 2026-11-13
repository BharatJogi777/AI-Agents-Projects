"""Create a timed, audience-aware presentation outline from supplied material."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Section:
    title: str
    key_message: str
    minutes: int
    evidence_refs: tuple[str, ...] = ()

def build_outline(topic: str, audience: str, sections: Iterable[Section], *, total_minutes: int) -> list[Section]:
    items = list(sections)
    if not topic.strip() or not audience.strip():
        raise ValueError("topic and audience are required")
    if total_minutes <= 0 or not items:
        raise ValueError("positive duration and at least one section are required")
    if any(not s.title.strip() or not s.key_message.strip() or s.minutes <= 0 for s in items):
        raise ValueError("sections need a title, key message and positive duration")
    if sum(s.minutes for s in items) > total_minutes:
        raise ValueError("section durations exceed presentation time")
    return items

def render_outline(topic: str, audience: str, sections: Iterable[Section], *, total_minutes: int) -> str:
    items = build_outline(topic, audience, sections, total_minutes=total_minutes)
    lines = [f"# {topic}", f"Audience: {audience}", f"Duration: {total_minutes} minutes", ""]
    for i, section in enumerate(items, 1):
        refs = ", ".join(section.evidence_refs) or "No source references supplied"
        lines.append(f"{i}. **{section.title}** ({section.minutes} min) — {section.key_message} [Evidence: {refs}]")
    return "\n".join(lines)
