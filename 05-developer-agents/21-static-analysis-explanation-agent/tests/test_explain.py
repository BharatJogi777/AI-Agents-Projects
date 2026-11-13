import pytest
from app.explain import explain_findings, to_json


def test_explains_and_preserves_scanner_evidence():
    item = {"rule_id": "S1", "severity": "high", "location": "src/a.py:3",
            "message": "Potential injection", "evidence": "query = user_input"}
    result = explain_findings([item])[0]
    assert result.evidence == item["evidence"]
    assert "significant" in result.impact
    assert '"verification_steps"' in to_json([result])


def test_rejects_unknown_severity_and_missing_fields():
    base = {"rule_id": "S1", "severity": "urgent", "location": "a.py:1", "message": "Issue"}
    with pytest.raises(ValueError):
        explain_findings([base])
    with pytest.raises(ValueError):
        explain_findings([{"rule_id": "S1"}])


def test_rejects_non_mapping():
    with pytest.raises(ValueError):
        explain_findings(["finding"])
