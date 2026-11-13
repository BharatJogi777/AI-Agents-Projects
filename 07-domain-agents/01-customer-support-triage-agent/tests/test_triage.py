from app.triage import triage_ticket
import pytest

def test_routes_urgent_technical_issue():
    result=triage_ticket("Login broken","Cannot access account; service down",customer_tier="premium")
    assert result.category=="technical" and result.priority=="urgent"

def test_rejects_invalid_tier():
    with pytest.raises(ValueError): triage_ticket("Help","Need support",customer_tier="gold")
