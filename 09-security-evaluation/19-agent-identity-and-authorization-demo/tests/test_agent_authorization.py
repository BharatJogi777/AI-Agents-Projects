from datetime import datetime, timezone, timedelta
import pytest
from app.agent_authorization import AgentGrant, authorize

def test_matching_identity_scope_and_expiry():
    now = datetime(2026,1,1,tzinfo=timezone.utc)
    grant = AgentGrant("agent-1", frozenset({"read"}), now + timedelta(minutes=1))
    assert authorize(grant, agent_id="agent-1", action="read", now=now)

def test_wrong_identity_and_scope_denied():
    now = datetime.now(timezone.utc)
    grant = AgentGrant("agent-1", frozenset({"read"}), now + timedelta(days=1))
    assert not authorize(grant, agent_id="agent-2", action="read", now=now)
    assert not authorize(grant, agent_id="agent-1", action="delete", now=now)

def test_naive_timestamp_rejected():
    grant = AgentGrant("a", frozenset({"x"}), datetime(2030,1,1))
    with pytest.raises(ValueError):
        authorize(grant, agent_id="a", action="x")
