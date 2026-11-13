import pytest
from app.events import explain_events

def test_groups_warning_events():
    event = {"namespace":"prod","kind":"Pod","name":"api-1","reason":"BackOff","message":"restarting","type":"Warning","last_timestamp":"2026-01-01T00:00:00Z"}
    result = explain_events([event, event])
    assert result[0].count == 2
    assert result[0].severity == "medium"
    assert "restart" in result[0].explanation.lower()

def test_rejects_missing_fields():
    with pytest.raises(ValueError): explain_events([{"name":"x"}])
