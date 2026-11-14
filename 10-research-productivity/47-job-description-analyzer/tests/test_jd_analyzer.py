from app.jd_analyzer import analyze_job_description
import pytest

def test_matches_whole_skill_terms():
    r=analyze_job_description("Requirements: Python and FastAPI experience.",["Python","FastAPI","Go"])
    assert r["matched_candidate_skills"]==["Python","FastAPI"]
    assert r["not_found_in_description"]==["Go"]

def test_empty_description_rejected():
    with pytest.raises(ValueError): analyze_job_description(" ",["Go"])

def test_empty_skill_rejected():
    with pytest.raises(ValueError): analyze_job_description("Python",[" "])
