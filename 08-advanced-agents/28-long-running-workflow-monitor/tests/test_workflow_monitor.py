import pytest
from app.workflow_monitor import StepSnapshot, inspect_workflow

def test_detects_timeout_and_failure():
    rows=inspect_workflow([StepSnapshot("a","running",12,10),StepSnapshot("b","failed",1,10)])
    assert [x.severity for x in rows] == ["high","high"]

def test_healthy_steps_have_no_findings():
    assert inspect_workflow([StepSnapshot("a","completed",2,10)]) == ()

def test_rejects_invalid_snapshot():
    with pytest.raises(ValueError): inspect_workflow([StepSnapshot("a","running",-1,10)])
    with pytest.raises(ValueError): inspect_workflow([StepSnapshot("a","pending",1,0)])
