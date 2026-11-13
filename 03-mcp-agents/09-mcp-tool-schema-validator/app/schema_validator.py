"""Fail-closed validation for a deliberately small JSON Schema subset."""
from __future__ import annotations

from typing import Any

SUPPORTED_TYPES = {"string", "number", "integer", "boolean", "null"}


class SchemaError(ValueError):
    pass


class ArgumentValidationError(ValueError):
    pass


def validate_schema(schema: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(schema, dict) or schema.get("type") != "object":
        raise SchemaError("root schema must be an object")
    allowed_root = {"type", "properties", "required", "additionalProperties"}
    if set(schema) - allowed_root:
        raise SchemaError("unsupported root schema keyword")
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    if not isinstance(properties, dict) or not isinstance(required, list):
        raise SchemaError("properties must be an object and required must be an array")
    if any(not isinstance(key, str) or not key for key in properties):
        raise SchemaError("property names must be non-empty strings")
    if any(key not in properties for key in required) or len(required) != len(set(required)):
        raise SchemaError("required must contain unique declared property names")
    if schema.get("additionalProperties", True) is not False and "additionalProperties" in schema:
        raise SchemaError("additionalProperties must be false in this policy profile")
    normalized = {"type": "object", "properties": {}, "required": list(required),
                  "additionalProperties": False}
    for name, spec in properties.items():
        if not isinstance(spec, dict) or spec.get("type") not in SUPPORTED_TYPES:
            raise SchemaError(f"unsupported property schema: {name}")
        if set(spec) - {"type", "minLength", "maxLength", "minimum", "maximum"}:
            raise SchemaError(f"unsupported constraints for property: {name}")
        if spec["type"] != "string" and ({"minLength", "maxLength"} & set(spec)):
            raise SchemaError("length constraints apply only to strings")
        if spec["type"] not in {"number", "integer"} and ({"minimum", "maximum"} & set(spec)):
            raise SchemaError("numeric constraints apply only to numbers")
        if "minLength" in spec and (not isinstance(spec["minLength"], int) or spec["minLength"] < 0):
            raise SchemaError("minLength must be a non-negative integer")
        if "maxLength" in spec and (not isinstance(spec["maxLength"], int) or spec["maxLength"] < 0):
            raise SchemaError("maxLength must be a non-negative integer")
        if spec.get("minLength", 0) > spec.get("maxLength", float("inf")):
            raise SchemaError("minLength cannot exceed maxLength")
        normalized["properties"][name] = dict(spec)
    return normalized


def validate_arguments(schema: dict[str, Any], arguments: Any) -> dict[str, Any]:
    schema = validate_schema(schema)
    if not isinstance(arguments, dict):
        raise ArgumentValidationError("arguments must be an object")
    properties = schema["properties"]
    unknown = set(arguments) - set(properties)
    if unknown:
        raise ArgumentValidationError(f"unknown properties: {', '.join(sorted(unknown))}")
    missing = set(schema["required"]) - set(arguments)
    if missing:
        raise ArgumentValidationError(f"missing required properties: {', '.join(sorted(missing))}")
    for name, value in arguments.items():
        spec = properties[name]
        kind = spec["type"]
        valid = {
            "string": lambda v: isinstance(v, str),
            "boolean": lambda v: isinstance(v, bool),
            "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
            "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
            "null": lambda v: v is None,
        }[kind](value)
        if not valid:
            raise ArgumentValidationError(f"{name} must be {kind}")
        if kind == "string":
            if len(value) < spec.get("minLength", 0) or len(value) > spec.get("maxLength", float("inf")):
                raise ArgumentValidationError(f"{name} violates string length constraints")
        if kind in {"number", "integer"}:
            if "minimum" in spec and value < spec["minimum"]:
                raise ArgumentValidationError(f"{name} is below minimum")
            if "maximum" in spec and value > spec["maximum"]:
                raise ArgumentValidationError(f"{name} exceeds maximum")
    return dict(arguments)
