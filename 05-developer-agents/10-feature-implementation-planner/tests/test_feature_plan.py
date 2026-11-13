import pytest

from app.feature_plan import plan_feature, to_json


def test_builds_phased_plan_and_preserves_scope_order():
    plan = plan_feature("Export", ["CSV export", "CSV export", "Access control"], ["Legacy clients"])
    assert plan.scope == ("CSV export", "Access control")
    assert [phase[0] for phase in plan.phases] == [
        "discovery", "design", "implementation", "verification", "release"
    ]
    assert plan.unresolved_constraints == ("Legacy clients",)
    assert '"quality_gates"' in to_json(plan)


def test_empty_requirements_still_produces_reviewable_plan():
    plan = plan_feature("New capability", [])
    assert plan.phases[2][1]


def test_validates_inputs():
    with pytest.raises(ValueError):
        plan_feature("", [])
    with pytest.raises(ValueError):
        plan_feature("Feature", [""])
    with pytest.raises(ValueError):
        plan_feature("Feature", [], [""])
