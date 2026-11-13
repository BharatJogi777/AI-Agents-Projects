from datetime import date,timedelta
import pytest
from app.onboarding import OnboardingTask,build_checklist
def test_overdue_and_required():
 r=build_checklist([OnboardingTask("IT","Laptop","IT",date(2026,1,2))],date(2026,1,1),date(2026,1,3))
 assert r["tasks"][0]["status"]=="overdue" and r["required_open"]==1
def test_duplicate_ids():
 with pytest.raises(ValueError): build_checklist([OnboardingTask("x","a","b",date(2026,1,2)),OnboardingTask("x","c","d",date(2026,1,3))],date(2026,1,1))
