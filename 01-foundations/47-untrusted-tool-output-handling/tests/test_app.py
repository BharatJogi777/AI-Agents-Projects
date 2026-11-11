import pytest
from app import ToolOutputNormalizer
def test_redaction_and_trust_label():
 r=ToolOutputNormalizer().normalize("lookup",{"api_key":"secret123","password":"p@ss"})
 assert r["trust"]=="untrusted" and "secret123" not in r["content"] and "p@ss" not in r["content"]
 assert r["content"].count("[REDACTED]")==2
def test_bound_and_invalid_limit():
 assert ToolOutputNormalizer(40).normalize("t",{"x":"z"*100})["truncated"]
 with pytest.raises(ValueError): ToolOutputNormalizer(10)
