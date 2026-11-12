from tool_output import *
def test_nested_credentials_are_redacted():
 e=ToolOutputNormalizer().normalize("lookup",{"data":[{"api_key":"abc","name":"safe"}],"Authorization":"Bearer xyz"})
 assert e.trust=="untrusted" and "[REDACTED]" in e.content and "abc" not in e.content and "safe" in e.content
def test_bounds_and_truncation_metadata():
 e=ToolOutputNormalizer(max_chars=32).normalize("tool",{"text":"x"*100})
 assert e.truncated and len(e.content)==32 and e.original_chars>32
def test_circular_and_unsupported_values_are_safe():
 x=[];x.append(x);e=ToolOutputNormalizer().normalize("tool",{"x":x,"obj":object()})
 assert "CIRCULAR_REFERENCE" in e.content and "UNSUPPORTED" in e.content
def test_invalid_tool_name():
 import pytest
 with pytest.raises(ToolOutputError):ToolOutputNormalizer().normalize("",{})
