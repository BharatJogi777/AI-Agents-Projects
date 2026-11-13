import pytest
from app.research_run import ResearchTask, checkpoint_run, resumable_tasks

def test_checkpoints_and_finds_resumable_tasks():
    run=checkpoint_run("r1",[ResearchTask("a","Find sources"),ResearchTask("b","Compare", "completed", ("url:1",))])
    assert resumable_tasks(run) == ("a",)

def test_rejects_completed_without_evidence():
    with pytest.raises(ValueError): checkpoint_run("r",[ResearchTask("a","Research","completed")])

def test_rejects_duplicate_ids_and_unknown_status():
    t=ResearchTask("a","Do")
    with pytest.raises(ValueError): checkpoint_run("r",[t,t])
    with pytest.raises(ValueError): checkpoint_run("r",[ResearchTask("b","Do","unknown")])
