import pytest
from app.collaboration import Collaboration, Role, Phase

def test_role_assignment_and_completion():
    c = Collaboration({"researcher": Role("researcher"), "critic": Role("critic", False)})
    c.assign("researcher", "agent-1")
    c.contribute("researcher", "agent-1", {"evidence": ["source"]})
    assert c.complete()["researcher"]["evidence"] == ["source"]
    assert c.phase == Phase.COMPLETE

def test_reject_wrong_agent_and_missing_required():
    c = Collaboration({"writer": Role("writer")})
    c.assign("writer", "w1")
    with pytest.raises(PermissionError): c.contribute("writer", "w2", {"draft": "x"})
    with pytest.raises(RuntimeError): c.complete()

def test_duplicate_assignment_and_closed_state():
    c = Collaboration({"writer": Role("writer")})
    c.assign("writer", "w1")
    with pytest.raises(ValueError): c.assign("writer", "w2")
    c.cancel()
    with pytest.raises(RuntimeError): c.assign("writer", "w1")
