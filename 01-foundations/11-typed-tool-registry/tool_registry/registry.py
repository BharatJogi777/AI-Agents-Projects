from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable, Type

from pydantic import BaseModel, ConfigDict, ValidationError

from .errors import ToolExecutionError, ToolRegistrationError

_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    args_model: Type[BaseModel]
    handler: Callable[[BaseModel], Any]

    def provider_schema(self) -> dict[str, Any]:
        return {"type": "function", "function": {
            "name": self.name, "description": self.description,
            "parameters": self.args_model.model_json_schema(),
        }}


class ToolRegistry:
    """Immutable-after-construction allowlist for trusted Python handlers.

    Register tools during application startup. Do not let model output or
    untrusted requests mutate this registry at runtime.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, name: str, description: str, args_model: Type[BaseModel],
                 handler: Callable[[BaseModel], Any]) -> None:
        if not isinstance(name, str) or not _NAME.fullmatch(name):
            raise ToolRegistrationError("tool name must match [a-z][a-z0-9_]{0,63}")
        if name in self._tools:
            raise ToolRegistrationError(f"duplicate tool: {name}")
        if not isinstance(description, str) or not description.strip() or len(description) > 1000:
            raise ToolRegistrationError("description must contain 1..1000 characters")
        if not isinstance(args_model, type) or not issubclass(args_model, BaseModel):
            raise ToolRegistrationError("args_model must be a Pydantic model class")
        if not callable(handler):
            raise ToolRegistrationError("handler must be callable")
        self._tools[name] = ToolSpec(name, description.strip(), args_model, handler)

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)

    def provider_schemas(self) -> list[dict[str, Any]]:
        return [spec.provider_schema() for spec in self._tools.values()]

    def execute(self, name: str, raw_arguments: Any) -> Any:
        spec = self._tools.get(name)
        if spec is None:
            raise ToolExecutionError("tool is not allowlisted")
        try:
            arguments = spec.args_model.model_validate(raw_arguments, strict=True)
        except ValidationError as exc:
            raise ToolExecutionError(f"invalid arguments for tool: {name}") from exc
        try:
            return spec.handler(arguments)
        except Exception as exc:
            # Preserve the cause for internal diagnostics; never return its text
            # to the model because it may contain credentials or internals.
            raise ToolExecutionError(f"tool handler failed: {name}") from exc
