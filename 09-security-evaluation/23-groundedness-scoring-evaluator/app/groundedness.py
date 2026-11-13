"""Transparent lexical grounding heuristic; not semantic entailment."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class GroundednessReport:
    score: float
    grounded_sentences: int
    total_sentences: int
    unsupported: tuple[str, ...]

def _terms(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zA-Z0-9]+", text.casefold()) if len(w) > 2}

def score_groundedness(answer: str, evidence: list[str], *, min_overlap: float = 0.3) -> GroundednessReport:
    if not isinstance(answer, str) or not answer.strip(): raise ValueError("answer must be non-empty")
    if not evidence or any(not isinstance(x, str) or not x.strip() for x in evidence):
        raise ValueError("evidence must contain non-empty strings")
    if not 0 < min_overlap <= 1: raise ValueError("min_overlap must be in (0, 1]")
    sentences=[s.strip() for s in re.split(r"(?<=[.!?])\s+", answer.strip()) if s.strip()]
    evidence_terms=_terms(" ".join(evidence))
    unsupported=[]
    for sentence in sentences:
        terms=_terms(sentence)
        ratio=(len(terms & evidence_terms) / len(terms)) if terms else 0.0
        if ratio < min_overlap: unsupported.append(sentence)
    total=len(sentences); grounded=total-len(unsupported)
    return GroundednessReport(grounded/total if total else 0.0, grounded, total, tuple(unsupported))
