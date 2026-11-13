import pytest
from app.takeover import HandoffState, initial_state, request_takeover, resolve_takeover

def test_human_can_resume_or_cancel():
    state=request_takeover(initial_state("w1"),reason="Captcha requires human")
    resumed=resolve_takeover(state,decision="resume",operator_id="operator-1")
    assert resumed.status == "automating"
    assert resumed.audit[-1] == "human_resume:operator-1"
    cancelled=resolve_takeover(state,decision="cancel",operator_id="operator-2")
    assert cancelled.status == "cancelled"

def test_rejects_invalid_transition_and_missing_reason():
    with pytest.raises(ValueError): request_takeover(initial_state("w"),reason=" ")
    waiting=request_takeover(initial_state("w"),reason="Review")
    with pytest.raises(ValueError): resolve_takeover(waiting,decision="approve",operator_id="u")
    with pytest.raises(ValueError): resolve_takeover(waiting,decision="resume",operator_id=" ")
