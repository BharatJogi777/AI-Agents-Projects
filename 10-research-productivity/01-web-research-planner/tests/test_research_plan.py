import pytest
from app.research_plan import build_research_plan

def test_plan_is_traceable_and_requires_confirmation():
    plan = build_research_plan(objective="vector databases", audience="backend engineers", scope="production systems")
    assert plan.requires_user_confirmation
    assert "URL" in plan.evidence_fields
    assert len(plan.research_questions) == 5

def test_question_limit_and_validation():
    assert len(build_research_plan(objective="x", audience="y", scope="z", max_questions=2).research_questions) == 2
    with pytest.raises(ValueError):
        build_research_plan(objective=" ", audience="y", scope="z")
    with pytest.raises(ValueError):
        build_research_plan(objective="x", audience="y", scope="z", max_questions=0)
