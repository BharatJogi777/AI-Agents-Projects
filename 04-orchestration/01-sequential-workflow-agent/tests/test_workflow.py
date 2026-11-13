import pytest
from app.workflow import SequentialWorkflow

def test_steps_run_in_order_and_share_state():
    flow = SequentialWorkflow([("a", lambda s: {"x": 2}), ("b", lambda s: {"y": s["x"] + 3})])
    result = flow.run({})
    assert result.state == {"x": 2, "y": 5}
    assert result.completed == ["a", "b"]
    assert result.failed_step is None

def test_retry_then_success():
    calls = {"n": 0}
    def flaky(state):
        calls["n"] += 1
        if calls["n"] == 1: raise RuntimeError("transient")
        return {"ok": True}
    result = SequentialWorkflow([("flaky", flaky)], max_retries=1).run({})
    assert result.state["ok"] is True

def test_failure_stops_later_steps():
    result = SequentialWorkflow([("bad", lambda s: 1 / 0), ("never", lambda s: {"x": 1})]).run({})
    assert result.failed_step == "bad"
    assert result.completed == []
