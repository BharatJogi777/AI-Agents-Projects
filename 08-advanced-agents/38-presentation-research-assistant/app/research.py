"""Build a source-attributed research brief; never invent missing evidence."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Evidence:
    source_id: str
    title: str
    url: str
    claim: str
    excerpt: str

@dataclass(frozen=True)
class ResearchBrief:
    topic: str
    evidence: tuple[Evidence, ...]
    gaps: tuple[str, ...]

def build_brief(topic: str, evidence: Iterable[Evidence], required_questions: Iterable[str] = ()) -> ResearchBrief:
    if not topic.strip():
        raise ValueError("topic is required")
    items = tuple(evidence)
    ids = [e.source_id for e in items]
    if len(ids) != len(set(ids)):
        raise ValueError("source_id values must be unique")
    for item in items:
        if not all(v.strip() for v in (item.source_id, item.title, item.url, item.claim, item.excerpt)):
            raise ValueError("each evidence item needs source, title, URL, claim and excerpt")
    gaps = tuple(q.strip() for q in required_questions if q.strip() and not any(q.casefold() in e.claim.casefold() for e in items))
    return ResearchBrief(topic.strip(), items, gaps)

def render_brief(brief: ResearchBrief) -> str:
    lines = [f"# Research brief: {brief.topic}", "", "## Findings"]
    lines.extend(f"- {e.claim} [Source: {e.source_id} — {e.title} — {e.url}]" for e in brief.evidence)
    lines.extend(["", "## Evidence gaps"])
    lines.extend(f"- {gap}" for gap in brief.gaps)
    if not brief.evidence:
        lines.append("- No evidence supplied; no findings can be stated.")
    return "\n".join(lines)
