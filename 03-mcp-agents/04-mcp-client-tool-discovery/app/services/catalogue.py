"""Pure policy layer for discovered MCP tool metadata."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


class CatalogueError(ValueError):
    """Raised when a server advertises invalid or ambiguous tool metadata."""


@dataclass(frozen=True, slots=True)
class DiscoveredTool:
    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass(frozen=True, slots=True)
class PublicTool:
    name: str
    description: str
    input_schema: dict[str, Any]


class ToolCatalogue:
    """Stores a validated snapshot and exposes only explicitly allowed tools."""

    def __init__(self, allowed_names: set[str], *, max_description_chars: int = 2_000) -> None:
        if not allowed_names or any(not self._valid_name(n) for n in allowed_names):
            raise ValueError("allowed_names must contain valid tool names")
        if max_description_chars < 1:
            raise ValueError("max_description_chars must be positive")
        self._allowed = frozenset(allowed_names)
        self._max_description_chars = max_description_chars
        self._tools: dict[str, PublicTool] = {}

    @staticmethod
    def _valid_name(name: object) -> bool:
        return isinstance(name, str) and 1 <= len(name) <= 128 and all(
            ch.isalnum() or ch in "_-" for ch in name
        )

    def replace(self, discovered: Iterable[DiscoveredTool]) -> None:
        candidate: dict[str, PublicTool] = {}
        for item in discovered:
            if not self._valid_name(item.name):
                raise CatalogueError("tool name must be 1-128 alphanumeric, underscore, or hyphen characters")
            if item.name in candidate:
                raise CatalogueError(f"duplicate tool name: {item.name}")
            if not isinstance(item.description, str):
                raise CatalogueError(f"description for {item.name} must be a string")
            if not isinstance(item.input_schema, dict):
                raise CatalogueError(f"input schema for {item.name} must be an object")
            if item.input_schema.get("type") not in (None, "object"):
                raise CatalogueError(f"input schema for {item.name} must describe an object")
            if len(item.description) > self._max_description_chars:
                raise CatalogueError(f"description for {item.name} exceeds configured limit")
            if item.name in self._allowed:
                candidate[item.name] = PublicTool(
                    name=item.name,
                    description=item.description,
                    input_schema=dict(item.input_schema),
                )
        self._tools = candidate

    def public_tools(self) -> list[PublicTool]:
        return [self._tools[name] for name in sorted(self._tools)]

    def get(self, name: str) -> PublicTool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise CatalogueError(f"tool is not discovered or not allowlisted: {name}") from exc
