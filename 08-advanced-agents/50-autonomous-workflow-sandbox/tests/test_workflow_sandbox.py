import pytest
from app.workflow_sandbox import Step, run_sandbox

def test_runs_registered_pure_steps_and_traces():
    state,trace=run_sandbox({"value":2},[Step("double","value","result")],registry={"double":lambda x:x*2})
    assert state["result"]==4 and trace[0].status=="completed"

def test_rejects_unregistered_step_and_missing_input():
    with pytest.raises(ValueError):
        run_sandbox({"x":1},[Step("shell","x","y")],registry={})
    with pytest.raises(KeyError):
        run_sandbox({},[Step("double","missing","y")],registry={"double":lambda x:x*2})
