import pytest
from app.remediate import suggest_remediations, to_json


def test_known_and_unknown_rules_get_guidance():
    items = suggest_remediations(["F401", "UP032", "XYZ"])
    assert "unused import" in items[0].guidance
    assert "modernization" in items[1].guidance
    assert "documentation" in items[2].guidance
    assert '"known_risk"' in to_json(items)


def test_deduplicates_rules():
    assert len(suggest_remediations(["F401", "F401"])) == 1


def test_rejects_invalid_rules():
    with pytest.raises(ValueError):
        suggest_remediations([""])
