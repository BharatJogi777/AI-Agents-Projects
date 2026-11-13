from app.cancellation import assess_cancellation
import pytest

def test_past_due_requires_billing_followup():
    result=assess_cancellation(subscription_id="sub-1",status="active",billing_state="past_due")
    assert any("billing" in x.lower() for x in result.required_actions)

def test_rejects_unknown_status():
    with pytest.raises(ValueError): assess_cancellation(subscription_id="sub-1",status="deleted",billing_state="current")
