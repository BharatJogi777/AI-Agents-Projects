import pytest
from app.task_completion import evaluate_completion

def test_complete_task():
    assert evaluate_completion({"saved","notified"},{"saved","notified"}).complete

def test_missing_requirement():
    r=evaluate_completion({"saved"},{"saved","notified"})
    assert r.completion_ratio == 0.5 and r.missing_requirements == ("notified",)

def test_prohibited_outcome_blocks_completion():
    assert not evaluate_completion({"saved","deleted"},{"saved"},{"deleted"}).complete

def test_invalid_set_argument():
    with pytest.raises(ValueError): evaluate_completion([],set())
