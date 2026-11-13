import pytest
from app.blackboard import Blackboard

def test_versioned_write_and_conflict():
    b = Blackboard()
    first = b.write("plan", {"step": 1}, "planner", expected_version=0)
    assert first.version == 1
    second = b.write("plan", {"step": 2}, "worker", expected_version=1)
    assert second.version == 2
    with pytest.raises(RuntimeError): b.write("plan", {}, "stale", expected_version=1)

def test_observations_do_not_overwrite_current():
    b = Blackboard()
    b.write("result", "approved", "reviewer")
    b.observe("result", "review note", "auditor")
    assert b.read("result").value == "approved"
    assert len(b.history("result")) == 2

def test_snapshot_is_copy():
    b = Blackboard(); b.write("x", 1, "a")
    snap = b.snapshot(); snap.clear()
    assert b.read("x") is not None
