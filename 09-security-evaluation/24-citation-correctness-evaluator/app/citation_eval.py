"""Citation registry and marker consistency checks."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class CitationIssue:
    code: str
    citation_id: str
    message: str

def evaluate_citations(answer: str, sources: dict[str, str]) -> tuple[CitationIssue, ...]:
    if not isinstance(answer, str): raise ValueError("answer must be a string")
    if not isinstance(sources, dict) or any(not isinstance(k, str) or not k.strip() or not isinstance(v, str) or not v.strip() for k,v in sources.items()):
        raise ValueError("sources must map non-empty IDs to non-empty descriptions")
    used=re.findall(r"\[([A-Za-z0-9_-]+)\]", answer)
    issues=[]
    for cid in used:
        if cid not in sources: issues.append(CitationIssue("unknown_citation",cid,"citation ID is absent from source registry"))
    for cid in sources:
        if cid not in used: issues.append(CitationIssue("unused_source",cid,"registered source is not cited"))
    return tuple(issues)
