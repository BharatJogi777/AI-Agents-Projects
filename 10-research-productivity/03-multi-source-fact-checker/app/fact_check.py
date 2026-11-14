"""Compare a claim with supplied evidence snippets using explainable lexical heuristics."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class FactCheck:
    verdict: str
    supporting_sources: tuple[str, ...]
    contradicting_sources: tuple[str, ...]
    insufficient_sources: tuple[str, ...]
    method: str = "Token overlap heuristic; human review is required."

def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2}

def check_claim(*, claim: str, evidence: list[dict], threshold: float = 0.35) -> FactCheck:
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("claim must be non-empty")
    if not isinstance(evidence, list):
        raise ValueError("evidence must be a list")
    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not 0 < threshold <= 1:
        raise ValueError("threshold must be in (0, 1]")
    terms = _tokens(claim)
    if not terms:
        raise ValueError("claim must contain searchable words")
    support, contradict, insufficient = [], [], []
    for item in evidence:
        if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k].strip() for k in ("source_id", "text", "stance")):
            raise ValueError("each evidence item needs source_id, text, and stance strings")
        overlap = len(terms & _tokens(item["text"])) / len(terms)
        target = support if item["stance"].lower() == "supports" else contradict if item["stance"].lower() == "contradicts" else insufficient
        if overlap >= threshold and item["stance"].lower() in ("supports", "contradicts"):
            target.append(item["source_id"])
        else:
            insufficient.append(item["source_id"])
    verdict = "mixed" if support and contradict else "supported" if support else "contradicted" if contradict else "insufficient evidence"
    return FactCheck(verdict, tuple(support), tuple(contradict), tuple(insufficient))
