from app.interview_prep import Competency,build_practice_plan
from datetime import date
import pytest
def test_prioritizes_skill_gaps():
 r=build_practice_plan([Competency("Go",2,5),Competency("SQL",4,3)],date(2026,12,1),date(2026,11,15))
 assert r["practice_items"][0]["competency"]=="Go" and r["days_until_interview"]==16
def test_past_date_rejected():
 with pytest.raises(ValueError): build_practice_plan([Competency("Go",2,5)],date(2026,1,1),date(2026,1,2))
def test_invalid_rating_rejected():
 with pytest.raises(ValueError): build_practice_plan([Competency("Go",0,5)],date(2026,12,1),date(2026,11,15))
