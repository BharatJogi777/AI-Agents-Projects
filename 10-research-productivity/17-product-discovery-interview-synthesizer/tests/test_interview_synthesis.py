import pytest
from app.interview_synthesis import synthesize_interviews

def test_groups_evidence_and_keeps_interview_ids():
    result=synthesize_interviews(interviews=[
        {"id":"I1","observations":[{"theme":"Onboarding","evidence":"Setup takes too long"}]},
        {"id":"I2","observations":[{"theme":"Onboarding","evidence":"I need guided setup"},{"theme":"Pricing","evidence":"Cost is unclear"}]},
    ])
    onboarding=next(x for x in result if x.name=="Onboarding")
    assert onboarding.evidence == ("Setup takes too long","I need guided setup")
    assert onboarding.interview_ids == ("I1","I2")

def test_rejects_observation_without_evidence():
    with pytest.raises(ValueError):
        synthesize_interviews(interviews=[{"id":"I1","observations":[{"theme":"UX","evidence":" "}]}])

def test_rejects_invalid_interview():
    with pytest.raises(ValueError, match="id"):
        synthesize_interviews(interviews=[{"observations":[]}])
