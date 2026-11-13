"""Draft a blameless postmortem from supplied incident facts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Postmortem:
    title: str
    summary: str
    impact: str
    timeline: tuple[str,...]
    confirmed_facts: tuple[str,...]
    hypotheses: tuple[str,...]
    follow_ups: tuple[str,...]

def draft_postmortem(*, title: str, summary: str, impact: str, timeline: list[str], confirmed_facts: list[str], hypotheses: list[str], follow_ups: list[str]) -> Postmortem:
    for name,value in (("title",title),("summary",summary),("impact",impact)):
        if not isinstance(value,str) or not value.strip(): raise ValueError(f"{name} is required")
    for name,items in (("timeline",timeline),("confirmed_facts",confirmed_facts),("hypotheses",hypotheses),("follow_ups",follow_ups)):
        if not isinstance(items,list) or any(not isinstance(x,str) or not x.strip() for x in items): raise ValueError(f"{name} must be a list of non-empty strings")
    if not timeline: raise ValueError("timeline must contain at least one event")
    if not confirmed_facts: raise ValueError("at least one confirmed fact is required")
    return Postmortem(title.strip(),summary.strip(),impact.strip(),tuple(timeline),tuple(confirmed_facts),tuple(hypotheses),tuple(follow_ups))
