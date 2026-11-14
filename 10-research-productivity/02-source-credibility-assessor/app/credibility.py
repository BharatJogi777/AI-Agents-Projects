"""Transparent source-quality heuristics; never declares a source truthful."""
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class CredibilityAssessment:
    score: int
    band: str
    strengths: tuple[str, ...]
    cautions: tuple[str, ...]
    disclaimer: str = "Heuristic quality assessment, not verification of factual accuracy."

def assess_source(*, has_named_author: bool, has_publication_date: bool, is_primary_source: bool,
                  cites_evidence: bool, has_corrections_policy: bool, conflicts_disclosed: bool) -> CredibilityAssessment:
    flags = (has_named_author, has_publication_date, is_primary_source, cites_evidence, has_corrections_policy, conflicts_disclosed)
    if any(not isinstance(v, bool) for v in flags):
        raise ValueError("all assessment inputs must be booleans")
    labels = ("named author", "publication date", "primary source", "evidence citations", "corrections policy", "conflicts disclosed")
    strengths = tuple(label for label, value in zip(labels, flags) if value)
    cautions = tuple(f"Not established: {label}" for label, value in zip(labels, flags) if not value)
    score = round(sum(flags) / len(flags) * 100)
    band = "strong signals" if score >= 80 else "mixed signals" if score >= 50 else "limited signals"
    return CredibilityAssessment(score, band, strengths, cautions)
