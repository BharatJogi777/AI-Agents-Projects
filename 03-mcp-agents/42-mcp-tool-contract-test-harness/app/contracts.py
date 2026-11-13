from __future__ import annotations
from typing import Any
from jsonschema import Draft202012Validator

def validate_tool_contract(tool: dict[str, Any]) -> list[str]:
    errors = []
    if not isinstance(tool.get("name"), str) or not tool["name"]:
        errors.append("tool name is required")
    schema = tool.get("inputSchema")
    if not isinstance(schema, dict):
        errors.append("inputSchema must be an object")
    else:
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"invalid input schema: {getattr(exc, 'message', type(exc).__name__)}")
    return errors

def validate_arguments(schema: dict[str, Any], arguments: dict[str, Any]) -> list[str]:
    return sorted(error.message for error in Draft202012Validator(schema).iter_errors(arguments))

def validate_result(result: Any, expected_type: type) -> None:
    if not isinstance(result, expected_type):
        raise TypeError(f"expected {expected_type.__name__}, got {type(result).__name__}")
