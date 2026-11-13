"""Small identity-bound authorization evaluator; it does not issue credentials."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class AgentGrant:
    agent_id: str
    scopes: frozenset[str]
    expires_at: datetime

def authorize(grant: AgentGrant | None, *, agent_id: str, action: str, now: datetime | None = None) -> bool:
    if grant is None or not agent_id or not action:
        return False
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None or grant.expires_at.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    return grant.agent_id == agent_id and action in grant.scopes and current < grant.expires_at
