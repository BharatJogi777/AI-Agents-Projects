from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Callable, Type

from pydantic import BaseModel, ValidationError

from .errors import ToolExecutionError, ToolRegistrationError

_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


@dataclass(frozen=True, slots=True)
class RegistryLimits:
    """Resource limits applied at the registry boundary."""

    max_tools: int = 64
    max_description_chars: int = 1_000
    max_result_bytes: int = 64 * 1024

    def __post_init__(self) -> None:
        for field_name in ("max_tools", "max_description_chars", "max_result_bytes"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{field_name} must be a positive integer")


@dataclass(frozen=True, slots=True)
class ToolSpec:
    """A trusted, startup-registered tool definition."""

    name: str
    description: str
    args_model: Type[BaseModel]
    handler: Callable[[BaseModel], Any]

    def provider_schema(self) -> dict[str, Any]:
        # JSON round-trip returns a detached JSON-compatible copy. Callers
        # cannot mutate the registry's internal schema/model definition.
        parameters = json.loads(json.dumps(self.args_model.model_json_schema()))
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": parameters,
            },
        }


class ToolRegistry:
    """Allowlist mapping provider tool names to trusted Python handlers.

    Register definitions during application startup, then call freeze().
    Model output can select a registered tool, but can never register code.
    """

    def __init__(self, limits: RegistryLimits | None = None) -> None:
        self._limits = limits or RegistryLimits()
        self._tools: dict[str, ToolSpec] = {}
        self._frozen = False

    @property
    def is_frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> None:
        """Prevent all later registration; safe to call more than once."""
        self._frozen = True

    def register(
        self,
        name: str,
        description: str,
        args_model: Type[BaseModel],
        handler: Callable[[BaseModel], Any],
    ) -> None:
        if self._frozen:
            raise ToolRegistrationError("registry is frozen")
        if not isinstance(name, str) or not _NAME.fullmatch(name):
            raise ToolRegistrationError("tool name must match [a-z][a-z0-9_]{0,63}")
        if name in self._tools:
            raise ToolRegistrationError(f"duplicate tool: {name}")
        if len(self._tools) >= self._limits.max_tools:
            raise ToolRegistrationError("maximum registered tool count reached")
        if (
            not isinstance(description, str)
            or not description.strip()
            or len(description) > self._limits.max_description_chars
        ):
            raise ToolRegistrationError(
                f"description must contain 1..{self._limits.max_description_chars} characters"
            )
        if not isinstance(args_model, type) or not issubclass(args_model, BaseModel):
            raise ToolRegistrationError("args_model must be a Pydantic model class")
        if not callable(handler):
            raise ToolRegistrationError("handler must be callable")

        spec = ToolSpec(name, description.strip(), args_model, handler)
        try:
            spec.provider_schema()
        except (TypeError, ValueError) as exc:
            raise ToolRegistrationError("argument model schema must be JSON serializable") from exc
        self._tools[name] = spec

    def names(self) -> tuple[str, ...]:
        """Return registered names in deterministic registration order."""
        return tuple(self._tools)

    def provider_schemas(self) -> list[dict[str, Any]]:
        """Return detached schemas suitable for an LLM provider request."""
        return [spec.provider_schema() for spec in self._tools.values()]

    def validate_arguments(self, name: str, raw_arguments: Any) -> BaseModel:
        spec = self._get_spec(name)
        if not isinstance(raw_arguments, Mapping):
            raise ToolExecutionError("tool arguments must be a JSON object")
        try:
            return spec.args_model.model_validate(dict(raw_arguments), strict=True)
        except ValidationError as exc:
            # Do not include rejected values or Pydantic's input repr in the
            # public error; those values may contain secrets or prompt attacks.
            raise ToolExecutionError(f"invalid arguments for tool: {name}") from exc

    def execute(self, name: str, raw_arguments: Any) -> Any:
        """Validate, invoke one allowlisted handler, and bound its JSON result."""
        spec = self._get_spec(name)
        arguments = self.validate_arguments(name, raw_arguments)
        try:
            result = spec.handler(arguments)
        except Exception as exc:
            raise ToolExecutionError(f"tool handler failed: {name}") from exc

        try:
            encoded = json.dumps(
                result,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            )
        except (TypeError, ValueError, RecursionError) as exc:
            raise ToolExecutionError(f"tool returned a non-JSON result: {name}") from exc
        if len(encoded.encode("utf-8")) > self._limits.max_result_bytes:
            raise ToolExecutionError(f"tool result exceeds byte limit: {name}")
        return json.loads(encoded)

    def _get_spec(self, name: str) -> ToolSpec:
        if not isinstance(name, str):
            raise ToolExecutionError("tool name must be a string")
        spec = self._tools.get(name)
        if spec is None:
            raise ToolExecutionError("tool is not allowlisted")
        return spec
