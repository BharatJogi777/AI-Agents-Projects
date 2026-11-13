"""Evidence-based conflict resolution with explicit policy and audit trail."""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Claim:
    agent_id: str
    value: str
    confidence: float
    evidence: tuple[str, ...]

@dataclass
class Resolution:
    winner: Claim
    rationale: str
    rejected: tuple[Claim, ...]
    audit: list[str] = field(default_factory=list)

def resolve(claims: list[Claim], minimum_confidence: float = 0.5) -> Resolution:
    if not claims:
        raise ValueError("at least one claim is required")
    if not 0 <= minimum_confidence <= 1:
        raise ValueError("minimum_confidence must be between 0 and 1")
    if any(not c.agent_id or not c.value or not 0 <= c.confidence <= 1 for c in claims):
        raise ValueError("claims require agent, value, and confidence in [0, 1]")
    eligible = [c for c in claims if c.confidence >= minimum_confidence and c.evidence]
    if not eligible:
        raise RuntimeError("no claim meets the evidence and confidence policy")
    winner = max(eligible, key=lambda c: (c.confidence, len(c.evidence), c.agent_id))
    rejected = tuple(c for c in claims if c != winner)
    return Resolution(winner, "Highest confidence among evidence-backed eligible claims",
                      rejected, [f"selected:{winner.agent_id}", f"rejected:{len(rejected)}"])
