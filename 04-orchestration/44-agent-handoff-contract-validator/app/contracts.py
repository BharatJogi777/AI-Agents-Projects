"""Validate agent handoff payloads against explicit, versioned contracts."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Field:
    name: str
    expected_type: type
    required: bool = True

@dataclass(frozen=True)
class HandoffContract:
    version: str
    fields: tuple[Field, ...]

    def validate(self, payload: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        if not self.version.strip():
            errors.append("contract version is required")
        known = {f.name for f in self.fields}
        for field in self.fields:
            if field.required and field.name not in payload:
                errors.append(f"missing required field: {field.name}")
            elif field.name in payload and not isinstance(payload[field.name], field.expected_type):
                errors.append(f"field {field.name} must be {field.expected_type.__name__}")
        for key in payload.keys() - known:
            errors.append(f"unexpected field: {key}")
        return errors

    def assert_valid(self, payload: dict[str, Any]) -> None:
        errors = self.validate(payload)
        if errors:
            raise ValueError("; ".join(errors))
