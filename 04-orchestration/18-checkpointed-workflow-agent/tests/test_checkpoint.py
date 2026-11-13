import pytest
from app.checkpoint import Checkpoint, CheckpointedWorkflow

def test_runs_steps_and_returns_checkpoint():
    flow = CheckpointedWorkflow([("a", lambda s: 2), ("b", lambda s: s["a"] * 3)])
    result = flow.run()
    assert result.outputs["b"] == 6 and result.next_step == 2

def test_resumes_from_valid_checkpoint():
    flow = CheckpointedWorkflow([("a", lambda s: 2), ("b", lambda s: s["a"] + 4)])
    saved = Checkpoint(("a",), {"a": 2}, 1)
    assert flow.run(checkpoint=saved).outputs["b"] == 6

def test_mismatched_checkpoint_rejected():
    flow = CheckpointedWorkflow([("a", lambda s: 1)])
    with pytest.raises(ValueError): flow.run(checkpoint=Checkpoint(("wrong",), {}, 1))
