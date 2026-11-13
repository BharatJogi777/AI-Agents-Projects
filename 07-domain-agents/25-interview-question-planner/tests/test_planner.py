import pytest
from app.planner import Competency, build_plan
def test_consistent_rubric():
 r=build_plan("Backend Engineer",[Competency("Concurrency","senior","concurrent systems")])
 assert len(r["questions"])==2 and len(r["questions"][0]["rubric"])==4 and r["automated_score"] is None
def test_invalid_count():
 with pytest.raises(ValueError): build_plan("Engineer",[Competency("Go","senior","Go")],0)
