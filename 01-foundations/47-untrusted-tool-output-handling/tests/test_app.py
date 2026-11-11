import json,pytest
from app import ToolOutputNormalizer
def test_redaction_and_trust_label():
 r=ToolOutputNormalizer().normalize("lookup",{"api_key":"secret123","password":"p@ss"})
 parsed=json.loads(r["content"])
 assert r["trust"]=="untrusted" and parsed["api_key"]=="[REDACTED]" and parsed["password"]=="[REDACTED]"
def test_bound_and_invalid_limit():
 assert ToolOutputNormalizer(40).normalize("t",{"x":"z"*100})["truncated"]
 with pytest.raises(ValueError): ToolOutputNormalizer(10)
