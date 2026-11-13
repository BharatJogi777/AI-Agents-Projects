import pytest
from app.contracts import validate_arguments, validate_result, validate_tool_contract

def test_valid_schema():
    assert validate_tool_contract({"name": "lookup", "inputSchema": {"type": "object"}}) == []

def test_invalid_schema_reported():
    assert validate_tool_contract({"name": "lookup", "inputSchema": {"type": "not-a-type"}})

def test_arguments_validated():
    schema = {"type": "object", "properties": {"count": {"type": "integer"}}, "required": ["count"]}
    assert validate_arguments(schema, {"count": "wrong"})

def test_result_type_enforced():
    with pytest.raises(TypeError):
        validate_result("ok", dict)
