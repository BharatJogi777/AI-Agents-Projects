import pytest
from app.budget import BudgetManager, Charge

def test_authorize_record_and_report():
    budget = BudgetManager(1.0)
    assert budget.authorize("agent-a", 0.7)
    assert not budget.authorize("agent-b", 1.1)
    budget.record(Charge("agent-a", 0.6))
    assert budget.report() == {"limit": 1.0, "spent": 0.6, "remaining": 0.4, "exceeded": False}

def test_overrun_and_invalid_charge():
    budget = BudgetManager(0.5); budget.record(Charge("a", 0.7))
    assert budget.exceeded and budget.remaining == 0
    with pytest.raises(ValueError): budget.record(Charge("", -1))
