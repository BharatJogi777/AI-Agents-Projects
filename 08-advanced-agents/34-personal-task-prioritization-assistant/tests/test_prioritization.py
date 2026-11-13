import pytest
from app.prioritization import Task, prioritize

def test_ranks_urgent_high_impact_work_first():
    rows=prioritize([Task("a","Routine",1,1,4,10),Task("b","Incident",5,5,1,0)])
    assert rows[0].task.task_id == "b"
    assert "urgency=5/5" in rows[0].reasons

def test_empty_list_is_valid():
    assert prioritize([]) == ()

def test_rejects_invalid_task_and_duplicate_ids():
    with pytest.raises(ValueError): prioritize([Task("x","Bad",6,1,1,0)])
    t=Task("x","Good",2,2,1,1)
    with pytest.raises(ValueError): prioritize([t,t])
