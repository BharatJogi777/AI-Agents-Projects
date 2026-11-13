import pytest
from app.plan import PlanStep, PlannerExecutor

def test_dependency_order_and_outputs():
    runner = PlannerExecutor({"a": lambda c: 2, "b": lambda c: c["a"] + 3})
    result = runner.run([PlanStep("a"), PlanStep("b", ("a",))])
    assert result.outputs == {"a": 2, "b": 5}

def test_failure_skips_dependent_node():
    runner = PlannerExecutor({"a": lambda c: 1 / 0, "b": lambda c: "no"})
    result = runner.run([PlanStep("a"), PlanStep("b", ("a",))])
    assert "a" in result.failures
    assert result.skipped == ("b",)

def test_cycle_and_unknown_dependencies_rejected():
    runner = PlannerExecutor({"a": lambda c: None, "b": lambda c: None})
    with pytest.raises(ValueError):
        runner.validate([PlanStep("a", ("b",)), PlanStep("b", ("a",))])
    with pytest.raises(ValueError):
        runner.validate([PlanStep("a", ("missing",))])
