import pytest
from app.screening import CandidateEvidence, compare
def test_job_skill_evidence_only():
 r=compare(["Go","SQL"],CandidateEvidence("C-1",("go",),{"go":"Built APIs"}))
 assert r["matched_job_skills"]==["go"] and r["hiring_decision"]=="human_review_required" and not r["protected_attributes_used"]
def test_requires_criteria():
 with pytest.raises(ValueError): compare([],CandidateEvidence("C",("Go",),{}))
