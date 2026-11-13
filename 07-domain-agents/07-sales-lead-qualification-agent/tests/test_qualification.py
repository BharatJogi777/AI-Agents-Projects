from app.qualification import qualify_lead
import pytest

def test_high_score_requires_complete_evidence():
    result=qualify_lead(company_fit=5,need=5,authority=5,timing=5,budget_confirmed=True)
    assert result.band=="high" and result.score==22

def test_rejects_out_of_range_score():
    with pytest.raises(ValueError): qualify_lead(company_fit=6,need=2,authority=2,timing=2)
