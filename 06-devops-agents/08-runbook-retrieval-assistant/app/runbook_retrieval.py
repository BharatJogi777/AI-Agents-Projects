"""Bounded lexical retrieval over curated runbook sections."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class RunbookSection:
    runbook_id: str
    title: str
    content: str
    reference: str

def retrieve_runbooks(query: str, sections: list[RunbookSection], *, limit: int = 5) -> list[dict]:
    if not query.strip(): raise ValueError("query must not be empty")
    if not 1 <= limit <= 20: raise ValueError("limit must be between 1 and 20")
    terms=set(re.findall(r"[a-z0-9_]+",query.lower()))
    results=[]
    for s in sections:
        if not s.runbook_id or not s.title or not s.reference: raise ValueError("runbook ID, title, and reference are required")
        title=set(re.findall(r"[a-z0-9_]+",s.title.lower())); body=set(re.findall(r"[a-z0-9_]+",s.content.lower()))
        score=3*len(terms&title)+len(terms&body)
        if score: results.append({"runbook_id":s.runbook_id,"title":s.title,"reference":s.reference,"score":score,"excerpt":s.content[:500]})
    return sorted(results,key=lambda x:(-x["score"],x["runbook_id"],x["reference"]))[:limit]
