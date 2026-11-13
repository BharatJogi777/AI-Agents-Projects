"""Assemble a daily briefing from user-supplied facts and source references."""
from dataclasses import dataclass

@dataclass(frozen=True)
class BriefItem:
    item_id: str
    category: str
    text: str
    source: str
    importance: int = 3

@dataclass(frozen=True)
class DailyBriefing:
    date: str
    sections: tuple[tuple[str, tuple[BriefItem, ...]], ...]

def build_briefing(date: str, items: list[BriefItem], *, max_per_section: int = 5) -> DailyBriefing:
    if not date.strip() or max_per_section < 1:
        raise ValueError("date and positive max_per_section are required")
    seen=set(); groups={}
    allowed={"calendar","tasks","updates","alerts"}
    for item in items:
        if not item.item_id.strip() or item.item_id in seen:
            raise ValueError("item IDs must be non-empty and unique")
        seen.add(item.item_id)
        if item.category not in allowed:
            raise ValueError("unsupported briefing category")
        if not item.text.strip() or not item.source.strip():
            raise ValueError("text and source are required")
        if not 1 <= item.importance <= 5:
            raise ValueError("importance must be between 1 and 5")
        groups.setdefault(item.category, []).append(item)
    sections=[]
    for category in ("alerts","calendar","tasks","updates"):
        ordered=sorted(groups.get(category,[]),key=lambda x:(-x.importance,x.item_id))
        if ordered:
            sections.append((category,tuple(ordered[:max_per_section])))
    return DailyBriefing(date,tuple(sections))
