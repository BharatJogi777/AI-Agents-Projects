import pytest

from app.issue_plan import create_plan, to_json


def test_extracts_requirements_and_security_risk():
    plan = create_plan("Add token endpoint", "The endpoint must validate token scopes.")
    assert plan.stated_requirements == ("The endpoint must validate token scopes.",)
    assert plan.acceptance_criteria[0].startswith("Verify:")
    assert any("security" in risk for risk in plan.risks)


def test_adds_concurrency_risk_and_open_questions():
    plan = create_plan("Queue worker", "Support parallel processing")
    assert plan.risks
    assert plan.open_questions
    assert '"suggested_test_cases"' in to_json(plan)


def test_rejects_bad_inputs():
    with pytest.raises(ValueError):
        create_plan("", "")
    with pytest.raises(TypeError):
        create_plan("Title", None)
