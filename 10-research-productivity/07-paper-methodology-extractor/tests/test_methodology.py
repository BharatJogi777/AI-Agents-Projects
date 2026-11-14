import pytest
from app.methodology import extract_methodology
def test_reports_unreported_fields():
 r=extract_methodology(study_design="cohort",sample_size=120,outcome_measures=["mortality"])
 assert r.sample_size==120 and "population" in r.unreported_fields
def test_rejects_invalid_sample_size_and_measure():
 with pytest.raises(ValueError): extract_methodology(sample_size=0)
 with pytest.raises(ValueError): extract_methodology(outcome_measures=[" "])
