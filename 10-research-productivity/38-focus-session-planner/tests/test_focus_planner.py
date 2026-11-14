from app.focus_planner import plan_focus_sessions
import pytest

def test_schedule_respects_available_time():
    blocks=plan_focus_sessions([("Write",50),("Review",20)],40,25,5)
    assert sum(b.minutes+b.break_after for b in blocks) <= 40
    assert sum(b.minutes for b in blocks) == 35

def test_invalid_estimate_rejected():
    with pytest.raises(ValueError):
        plan_focus_sessions([("Task",0)],30)

def test_empty_tasks_returns_empty():
    assert plan_focus_sessions([],30) == []
