import pytest

from app.schema_validator import (
    ArgumentValidationError, SchemaError, validate_arguments, validate_schema,
)

SCHEMA = {
    "type": "object",
    "properties": {
        "order_id": {"type": "string", "minLength": 1, "maxLength": 20},
        "limit": {"type": "integer", "minimum": 1, "maximum": 100},
        "active": {"type": "boolean"},
    },
    "required": ["order_id"],
    "additionalProperties": False,
}


def test_valid_arguments_are_returned_unchanged():
    value = {"order_id": "ORD-42", "limit": 10, "active": True}
    assert validate_arguments(SCHEMA, value) == value


@pytest.mark.parametrize("args", [
    [],
    {"order_id": ""},
    {"order_id": "ORD-1", "extra": 1},
    {"order_id": "ORD-1", "limit": True},
    {"order_id": "ORD-1", "limit": 101},
    {},
])
def test_invalid_arguments_fail(args):
    with pytest.raises(ArgumentValidationError):
        validate_arguments(SCHEMA, args)


def test_unsupported_nested_schema_fails_closed():
    with pytest.raises(SchemaError):
        validate_schema({"type": "object", "properties": {"meta": {"type": "object"}}})


def test_unknown_schema_keyword_is_rejected():
    with pytest.raises(SchemaError):
        validate_schema({"type": "object", "patternProperties": {}})


def test_duplicate_required_property_is_rejected():
    schema = {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id", "id"]}
    with pytest.raises(SchemaError):
        validate_schema(schema)
