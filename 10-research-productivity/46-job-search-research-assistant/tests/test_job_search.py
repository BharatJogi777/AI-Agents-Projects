from app.job_search import JobLead, organize_leads
import pytest

def test_deduplicates_but_preserves_source():
    leads=[JobLead("Acme","Backend Engineer","Referral",location="Bengaluru"),JobLead("acme","backend engineer","Careers page",location="bengaluru")]
    result=organize_leads(leads)
    assert len(result)==1 and result[0]["source"]=="Referral"

def test_invalid_status_rejected():
    with pytest.raises(ValueError): organize_leads([JobLead("A","Role","Source",status="hired")])

def test_missing_source_rejected():
    with pytest.raises(ValueError): organize_leads([JobLead("A","Role"," ")])
