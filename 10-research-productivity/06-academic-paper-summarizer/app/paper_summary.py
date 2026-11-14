"""Create a structured summary from explicitly supplied paper sections."""
from dataclasses import dataclass
@dataclass(frozen=True)
class PaperSummary:
    objective: str
    methods: str
    findings: str
    limitations: str
    open_questions: tuple[str,...]
    source_id: str
def summarize_paper(*, source_id: str, abstract: str, methods: str, findings: str, limitations: str) -> PaperSummary:
    values={"source_id":source_id,"abstract":abstract,"methods":methods,"findings":findings,"limitations":limitations}
    if any(not isinstance(v,str) or not v.strip() for v in values.values()):
        raise ValueError("all paper sections and source_id must be non-empty strings")
    questions=tuple(x for x in ("Were findings independently replicated?","How generalizable are the results?","What biases or confounders remain?") if x)
    return PaperSummary(abstract.strip(),methods.strip(),findings.strip(),limitations.strip(),questions,source_id.strip())
