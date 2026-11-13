"""Evidence-set based claim evaluation; not an autonomous truth detector."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ClaimResult:
    claim: str
    status: str
    matched_evidence: str | None = None

def evaluate_claims(claims: list[str], evidence: list[str]) -> tuple[ClaimResult, ...]:
    if any(not isinstance(x, str) or not x.strip() for x in claims + evidence):
        raise ValueError("claims and evidence must contain non-empty strings")
    normalized = [(e.casefold(), e) for e in evidence]
    results=[]
    for claim in claims:
        needle=claim.casefold()
        exact=next(((raw, original) for raw, original in normalized if needle in raw or raw in needle), None)
        if exact:
            results.append(ClaimResult(claim, "supported", exact[1])); continue
        # Contradiction is only asserted for explicit paired negation of the same phrase.
        opposite=None
        for raw, original in normalized:
            if raw.startswith("not ") and raw[4:] == needle: opposite=original
            elif needle.startswith("not ") and needle[4:] == raw: opposite=original
        results.append(ClaimResult(claim, "contradicted" if opposite else "unverified", opposite))
    return tuple(results)
