from app.impact_classifier import classify_action

def test_classifies_money_transfer_as_critical():
    result = classify_action(action="transfer funds",indicators=["money_transfer"])
    assert result["impact"] == "critical" and result["requires_human_review"]

def test_rejects_unknown_indicator():
    import pytest
    with pytest.raises(ValueError): classify_action(action="x",indicators=["unknown"])
