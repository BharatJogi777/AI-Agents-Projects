import pytest
from app import *
def test_redaction_and_trust_label():
 r=ToolOutputNormalizer().normalize("lookup",{"api_key":"secret123"})
 assert r["trust"]=="untrusted" and "secret123" not in r["content"] and "[REDACTED]" in r["content"]
def test_bounds():
 assert ToolOutputNormalizer(40).normalize("t",{"x":"z"*100})["truncated"]
 with pytest.raises(ValueError): ToolOutputNormalizer(10)
