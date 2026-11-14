from app.workload import WorkItem, prioritize
import pytest

def test_rank_explains_blocking_priority():
    items=[WorkItem("a","Routine",1,1,2),WorkItem("b","Unblock",3,3,1,True)]
    ranked=prioritize(items)
    assert ranked[0]["item"].id == "b"
    assert "blocks other work" in ranked[0]["reasons"]

def test_invalid_scale_rejected():
    with pytest.raises(ValueError):
        prioritize([WorkItem("x","Bad",6,2,1)])

def test_duplicate_ids_rejected():
    item=WorkItem("x","Task",1,1,1)
    with pytest.raises(ValueError, match="duplicate"):
        prioritize([item,item])
