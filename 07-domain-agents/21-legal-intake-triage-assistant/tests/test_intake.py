from datetime import date
import pytest
from app.intake import Intake, triage
def test_urgent_and_missing_fields():
 r=triage(Intake("contract","Review terms",date(2026,1,1),date(2026,1,5)),date(2026,1,2))
 assert r["urgency"]=="urgent" and "jurisdiction" in r["missing_fields"] and r["human_review_required"]
def test_invalid_deadline():
 with pytest.raises(ValueError): triage(Intake("x","y",date(2026,1,5),date(2026,1,4)))
