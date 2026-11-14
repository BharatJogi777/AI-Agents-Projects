from app.grant_finder import Grant,find_grants
from datetime import date
import pytest
def test_filters_grants():
 gs=[Grant("a","Open",("AI",),("nonprofit",),100,500,date(2027,1,1)),Grant("b","Expired",("AI",),("nonprofit",),100,500,date(2025,1,1))]
 assert [g.id for g in find_grants(gs,applicant_type="nonprofit",topic="AI",budget=300,as_of=date(2026,1,1))]==["a"]
def test_bad_range_rejected():
 with pytest.raises(ValueError): find_grants([Grant("x","Bad",("AI",),("nonprofit",),500,100,None)],applicant_type="nonprofit",topic="AI",budget=300,as_of=date.today())
def test_empty_catalogue():
 assert find_grants([],applicant_type="company",topic="health",budget=0,as_of=date.today())==[]
