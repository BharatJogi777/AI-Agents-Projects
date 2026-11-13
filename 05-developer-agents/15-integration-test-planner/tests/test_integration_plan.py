import pytest
from app.integration_plan import plan_integration_tests, to_json


def test_generates_three_scenarios_per_dependency():
    scenarios = plan_integration_tests(["api", "payments"], {"api": ["payments"]})
    assert len(scenarios) == 3
    assert {item.name.rsplit("_", 1)[-1] for item in scenarios} == {"success", "timeout", "failure"}
    assert '"cleanup"' in to_json(scenarios)


def test_no_dependencies_returns_empty_plan():
    assert plan_integration_tests(["worker"], {}) == []


def test_rejects_unknown_and_duplicate_services():
    with pytest.raises(ValueError):
        plan_integration_tests(["api"], {"api": ["database"]})
    with pytest.raises(ValueError):
        plan_integration_tests(["api", "api"], {})
