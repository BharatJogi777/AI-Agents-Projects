import pytest
from app.tracing import TraceRecorder

def test_parent_child_trace_and_duration():
    r=TraceRecorder(); r.record("t","root","workflow",started_at=1,ended_at=5)
    r.record("t","child","tool",parent_id="root",started_at=2,ended_at=3)
    assert len(r.for_trace("t")) == 2 and r.critical_path_duration("t") == 4

def test_invalid_parent_and_duplicate():
    r=TraceRecorder()
    with pytest.raises(ValueError): r.record("t","x","x",parent_id="missing")
    r.record("t","x","x",started_at=0,ended_at=0)
    with pytest.raises(ValueError): r.record("t","x","x",started_at=0,ended_at=0)
