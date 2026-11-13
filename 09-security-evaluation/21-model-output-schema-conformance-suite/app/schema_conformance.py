"""Deterministic validation for model outputs against a bounded schema subset."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Violation:
    path: str
    code: str
    message: str

def validate_output(value: Any, schema: dict[str, Any]) -> tuple[Violation, ...]:
    """Support object, array, string, integer, number, boolean, null, required and enum."""
    if not isinstance(schema, dict) or "type" not in schema:
        raise ValueError("schema must be an object with a type")
    found: list[Violation] = []
    def walk(item: Any, spec: dict[str, Any], path: str) -> None:
        kind = spec["type"]
        checks = {"object": lambda x: isinstance(x, dict), "array": lambda x: isinstance(x, list),
                  "string": lambda x: isinstance(x, str), "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
                  "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
                  "boolean": lambda x: isinstance(x, bool), "null": lambda x: x is None}
        if kind not in checks: raise ValueError(f"unsupported schema type: {kind}")
        if not checks[kind](item):
            found.append(Violation(path, "type", f"expected {kind}")); return
        if "enum" in spec and item not in spec["enum"]:
            found.append(Violation(path, "enum", "value is not an allowed enum member"))
        if kind == "object":
            props = spec.get("properties", {})
            if not isinstance(props, dict): raise ValueError("properties must be an object")
            for key in spec.get("required", []):
                if key not in item: found.append(Violation(f"{path}.{key}", "required", "required property is missing"))
            for key, child in props.items():
                if key in item: walk(item[key], child, f"{path}.{key}")
            if spec.get("additionalProperties") is False:
                for key in item.keys() - props.keys(): found.append(Violation(f"{path}.{key}", "additional", "unexpected property"))
        if kind == "array" and "items" in spec:
            for i, child in enumerate(item): walk(child, spec["items"], f"{path}[{i}]")
    walk(value, schema, "$")
    return tuple(found)
