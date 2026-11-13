import pytest
from app.conflict import Claim, resolve

def test_evidence_backed_high_confidence_claim_wins():
    a=Claim("a","x",.8,("log",)); b=Claim("b","y",.9,("trace","metric"))
    assert resolve([a,b]).winner == b

def test_reject_unsupported_claims():
    with pytest.raises(RuntimeError):
        resolve([Claim("a","x",.99,())])
    with pytest.raises(ValueError): resolve([])
