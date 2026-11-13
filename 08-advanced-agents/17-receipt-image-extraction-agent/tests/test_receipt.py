import pytest
from app.receipt import Receipt,validate_receipt
def test_flags_arithmetic_mismatch():
 r=validate_receipt(Receipt("Shop","2026-01-01","usd",10,2,15,.99))
 assert r["requires_review"] and not r["arithmetic_consistent"]
def test_accepts_consistent_receipt():
 r=validate_receipt(Receipt("Shop","2026-01-01","INR",10,1,11,.99))
 assert not r["requires_review"]
def test_rejects_invalid_confidence():
 with pytest.raises(ValueError): validate_receipt(Receipt("S","d","USD",1,0,1,2))
