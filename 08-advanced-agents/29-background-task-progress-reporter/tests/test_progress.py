import pytest
from app.progress import Milestone, calculate_progress

def test_weighted_progress_and_exceptions():
    result=calculate_progress([Milestone("a",3,"completed"),Milestone("b",1,"blocked")])
    assert result.percent == 75
    assert result.blocked == ("b",)

def test_all_pending_is_zero():
    assert calculate_progress([Milestone("a",1,"pending")]).percent == 0

def test_rejects_invalid_milestones():
    with pytest.raises(ValueError): calculate_progress([])
    with pytest.raises(ValueError): calculate_progress([Milestone("a",0,"pending")])
    with pytest.raises(ValueError): calculate_progress([Milestone("a",1,"unknown")])
