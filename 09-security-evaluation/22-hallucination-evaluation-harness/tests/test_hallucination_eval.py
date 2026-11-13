import pytest
from app.hallucination_eval import evaluate_claims

def test_supported_claim():
    r=evaluate_claims(["The service is healthy"],["The service is healthy"])
    assert r[0].status == "supported"

def test_unverified_claim_is_not_called_false():
    assert evaluate_claims(["Revenue doubled"],["Revenue was stable"])[0].status == "unverified"

def test_explicit_negation_conflict():
    assert evaluate_claims(["not ready"],["ready"])[0].status == "contradicted"

def test_rejects_empty_claim():
    with pytest.raises(ValueError): evaluate_claims([" "],[])
