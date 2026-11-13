from app.response import draft_response
import pytest

def test_uses_only_supplied_facts():
    result=draft_response("Asha","late delivery",["Carrier scan shows delay"],["We will check with the carrier"])
    assert "Carrier scan shows delay" in result.body and result.requires_agent_review

def test_rejects_empty_issue():
    with pytest.raises(ValueError): draft_response("Asha","",[],[])
