import pytest
from app.schema_conformance import validate_output

SCHEMA={"type":"object","required":["answer"],"properties":{"answer":{"type":"string"},"score":{"type":"number"}},"additionalProperties":False}

def test_valid_output():
    assert validate_output({"answer":"ok","score":0.8}, SCHEMA) == ()

def test_reports_multiple_violations():
    result=validate_output({"score":"high","extra":1}, SCHEMA)
    assert {v.code for v in result} == {"required","type","additional"}

def test_boolean_is_not_integer():
    assert validate_output(True, {"type":"integer"})[0].code == "type"

def test_rejects_unknown_schema_type():
    with pytest.raises(ValueError): validate_output("x", {"type":"magic"})
