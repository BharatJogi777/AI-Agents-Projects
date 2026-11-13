import pytest
from app.replanner import PlanAndReplan, Step

def test_replans_remaining_work_from_latest_state():
    calls = {"bad": 0}
    def flaky(state):
        calls["bad"] += 1
        if calls["bad"] == 1: raise RuntimeError("temporary")
        return {"finished": True}
    def planner(state, completed):
        if "prepare" not in completed:
            return [Step("prepare", lambda s: {"ready": True}), Step("unstable", flaky)]
        return [Step("finish", lambda s: {"done": s["ready"]})]
    result = PlanAndReplan(planner, max_replans=1).run({})
    assert result.completed == ("prepare", "finish")
    assert result.state["done"] is True
    assert result.replans == 1

def test_replan_budget_exhaustion_returns_failure():
    planner = lambda s, c: [Step("fails", lambda _: 1 / 0)]
    result = PlanAndReplan(planner, max_replans=0).run({})
    assert result.failed == "fails"

def test_duplicate_or_repeated_step_rejected():
    planner = lambda s, c: [Step("x", lambda _: {}) , Step("x", lambda _: {})]
    with pytest.raises(ValueError): PlanAndReplan(planner).run({})
