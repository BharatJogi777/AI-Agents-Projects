from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ToolRecord:
    server: str
    name: str
    description: str
    version: str
    input_schema: dict[str, Any]

    def validate(self) -> None:
        if not all(value.strip() for value in (self.server, self.name, self.version)):
            raise ValueError("server, name, and version are required")
        if not isinstance(self.input_schema, dict) or self.input_schema.get("type") != "object":
            raise ValueError("input_schema must be an object schema")
        properties = self.input_schema.get("properties", {})
        required = self.input_schema.get("required", [])
        if not isinstance(properties, dict) or not isinstance(required, list):
            raise ValueError("invalid schema properties or required fields")
        if not set(required).issubset(properties):
            raise ValueError("required fields must exist in properties")


class ToolRegistry:
    def __init__(self):
        self._records: dict[tuple[str, str], ToolRecord] = {}

    def register(self, record: ToolRecord) -> None:
        record.validate()
        key = (record.server, record.name)
        if key in self._records:
            raise ValueError(f"duplicate tool registration: {record.server}/{record.name}")
        self._records[key] = record

    def find(self, *, server: str | None = None, name: str | None = None) -> list[ToolRecord]:
        return sorted(
            (r for r in self._records.values()
             if (server is None or r.server == server) and (name is None or r.name == name)),
            key=lambda r: (r.server, r.name),
        )

    def export(self) -> list[dict[str, Any]]:
        return [asdict(record) for record in self.find()]
