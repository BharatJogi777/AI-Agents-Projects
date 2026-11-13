import pytest

from app.triage import classify_issue, to_json


def test_security_issue_gets_high_priority_and_evidence():
    result = classify_issue("Authentication bypass vulnerability")
    assert result.category == "security"
    assert result.urgency == "high"
    assert result.evidence


def test_production_outage_is_critical():
    assert classify_issue("Production down", "service unavailable").urgency == "critical"


def test_unknown_issue_is_sent_to_triage():
    result = classify_issue("Question")
    assert result.category == "needs-triage"
    assert result.routing_hint == "triage-queue"
    assert '"confidence"' in to_json(result)


def test_invalid_input():
    with pytest.raises(ValueError):
        classify_issue("")
