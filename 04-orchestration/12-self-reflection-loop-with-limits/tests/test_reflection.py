import pytest
from app.reflection import ReflectionLoop

def test_loop_stops_when_accepted():
    flow = ReflectionLoop(lambda task, feedback: len(feedback), lambda out: (out >= 1, "review"), 4)
    result = flow.run("do task")
    assert result.accepted and result.attempts == 2

def test_loop_respects_attempt_limit():
    result = ReflectionLoop(lambda t, f: "x", lambda o: (False, "again"), 2).run("task")
    assert result.attempts == 2 and not result.accepted

def test_blank_task_rejected():
    with pytest.raises(ValueError):
        ReflectionLoop(str, lambda o: (True, ""), 1).run(" ")
