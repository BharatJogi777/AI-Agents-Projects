from datetime import date,timedelta
import pytest
from app.coach import Goal,coach_plan
def test_prioritizes_goals_and_totals_hours():
 d=date(2026,1,1)
 r=coach_plan([Goal("G","Learn Python",d+timedelta(days=7),3,5)],d)
 assert r["goals"][0]["status"]=="due_soon" and r["total_weekly_hours"]==3
def test_rejects_past_deadline():
 d=date(2026,1,1)
 with pytest.raises(ValueError): coach_plan([Goal("G","Goal",d-timedelta(days=1),2,2)],d)
