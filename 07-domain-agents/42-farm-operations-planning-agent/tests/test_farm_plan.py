from datetime import date
import pytest
from app.planning import Task,validate_plan
def test_detects_worker_overallocation():
 d=date(2026,6,1); t=Task("T1","F1","sowing",d,4,3)
 assert len(validate_plan([t],{d:2})["capacity_conflicts"])==1
def test_rejects_duplicate_task():
 d=date(2026,6,1); t=Task("T","F","spray",d,2,1)
 with pytest.raises(ValueError): validate_plan([t,t],{d:2})
