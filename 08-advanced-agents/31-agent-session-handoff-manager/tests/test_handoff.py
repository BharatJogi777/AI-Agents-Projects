import pytest
from app.handoff import create_handoff

def test_creates_portable_handoff():
    h=create_handoff(session_id="s1",objective="Ship API",completed=["schema"],pending=["tests"],constraints=["no prod writes"])
    assert h.pending == ("tests",)
    assert "no prod writes" in h.constraints

def test_rejects_conflicting_or_empty_handoff():
    with pytest.raises(ValueError): create_handoff(session_id="s",objective="x",completed=["a"],pending=["a"],constraints=[])
    with pytest.raises(ValueError): create_handoff(session_id=" ",objective="x",completed=["a"],pending=[],constraints=[])
    with pytest.raises(ValueError): create_handoff(session_id="s",objective="x",completed=[],pending=[],constraints=[])
