# AG-109 — MCP tool schema validator

Validate discovered MCP input schemas before exposing tools to an agent. This deliberately supports a conservative JSON Schema subset so unsupported constructs fail closed rather than being silently ignored.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Supported schema subset

Object root, properties, required, additionalProperties, and primitive string/number/integer/boolean/null types. String length and numeric bounds are enforced. Nested objects and arrays are intentionally rejected in this first version.

## Example

```python
from app.schema_validator import validate_schema, validate_arguments

schema = validate_schema({
    "type": "object",
    "properties": {"order_id": {"type": "string", "minLength": 1}},
    "required": ["order_id"],
    "additionalProperties": False,
})
validate_arguments(schema, {"order_id": "ORD-42"})
```

The validator is a local policy gate; it does not replace validation performed by the MCP server itself.
