import pytest
from app.fact_check import check_claim

def test_supported_and_mixed_verdicts():
    claim = "the service uses encrypted database storage"
    result = check_claim(claim=claim, evidence=[{"source_id":"a","text":"The service uses encrypted database storage","stance":"supports"}])
    assert result.verdict == "supported"
    mixed = check_claim(claim=claim, evidence=[
        {"source_id":"a","text":"The service uses encrypted database storage","stance":"supports"},
        {"source_id":"b","text":"The service uses encrypted database storage","stance":"contradicts"}])
    assert mixed.verdict == "mixed"

def test_unknown_stance_and_invalid_claim_are_not_support():
    result = check_claim(claim="database encryption", evidence=[{"source_id":"x","text":"database encryption","stance":"unknown"}])
    assert result.verdict == "insufficient evidence"
    with pytest.raises(ValueError):
        check_claim(claim=" ", evidence=[])
