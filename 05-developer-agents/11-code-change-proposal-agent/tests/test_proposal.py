import pytest
from app.proposal import create_proposal, to_json


def test_proposal_links_actions_to_observations():
    result = create_proposal("Refactor validation", ["Two handlers duplicate validation"])
    assert len(result.changes) == 1
    assert "duplicate" in result.changes[0].rationale
    assert any("human approval" in gate for gate in result.review_gates)


def test_empty_observations_require_discovery():
    result = create_proposal("Improve reliability", [])
    assert result.changes == ()
    assert "discovery" in result.assumptions[0]
    assert '"goal"' in to_json(result)


def test_validation():
    with pytest.raises(ValueError):
        create_proposal("", [])
    with pytest.raises(ValueError):
        create_proposal("Goal", [""])
