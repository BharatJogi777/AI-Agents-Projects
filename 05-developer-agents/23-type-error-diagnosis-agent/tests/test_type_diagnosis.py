import pytest
from app.type_diagnosis import diagnose, to_json


def test_classifies_common_diagnostics():
    results = diagnose(["Item has no attribute 'id'", "Incompatible assignment", "Value may be None"])
    assert [x.category for x in results] == ["missing-attribute", "assignment", "optional-value"]
    assert '"next_steps"' in to_json(results)


def test_unknown_diagnostic_is_preserved():
    result = diagnose(["Some new checker diagnostic"])[0]
    assert result.category == "unclassified"
    assert "original checker" in result.likely_cause


def test_rejects_empty_message():
    with pytest.raises(ValueError):
        diagnose([""])
