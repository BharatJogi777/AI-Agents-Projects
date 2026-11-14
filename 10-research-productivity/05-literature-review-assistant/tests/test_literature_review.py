import pytest
from app.literature_review import build_review_outline

def test_groups_studies_and_detects_duplicate_doi():
    result = build_review_outline(studies=[
        {"study_id":"S1","title":"A","theme":"retrieval","limitations":"small sample","doi":"10/x"},
        {"study_id":"S2","title":"B","theme":"retrieval","limitations":"single domain","doi":"10/X"},
        {"study_id":"S3","title":"C","theme":"generation","limitations":"short duration"}])
    assert result.included_study_ids == ("S1", "S3")
    assert result.duplicate_study_ids == ("S2",)
    assert result.themes[0][0] == "generation"

def test_invalid_study_is_rejected():
    with pytest.raises(ValueError):
        build_review_outline(studies=[{"study_id":"S1"}])
