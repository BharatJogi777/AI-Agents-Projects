from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel, ValidationError

from .errors import ToolCallRejected, ToolHandlerFailed

_TOOL_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


@dataclass(frozen=True, slots=True)
class GateLimits:
    max_argument_bytes: int = 16_384
    max_result_bytes: int = 64 * 1024
    max_feedback_items: int = 8

    def __post_init__(self) -> None:
        if not 128 <= self.max_argument_bytes <= 1_000_000:
            raise ValueError("max_argument_bytes must be 128..1000000")
        if not 128 <= self.max_result_bytes <= 1_000_000:
            raise ValueError("max_result_bytes must be 128..1000000")
        if not 1 <= self.max_feedback_items <= 20:
            raise ValueError("max_feedback_items must be 1..20")


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


class ArgumentGate:
    """Fail-closed boundary between model-generated arguments and handlers."""

    def __init__(
        self,
        schemas: dict[str, type[BaseModel]],
        handlers: dict[str, Callable[[BaseModel], Any]],
        *,
        max_argument_bytes: int = 16_384,
        max_feedback_items: int = 8,
        max_result_bytes: int = 64 * 1024,
        limits: GateLimits | None = None,
    ) -> None:
        if limits is not None and (
            max_argument_bytes != 16_384
            or max_feedback_items != 8
            or max_result_bytes != 64 * 1024
        ):
            raise ValueError("pass either limits or individual limit arguments, not both")
        self._limits = limits or GateLimits(
            max_argument_bytes=max_argument_bytes,
            max_feedback_items=max_feedback_items,
            max_result_bytes=max_result_bytes,
        )
        if not isinstance(schemas, dict) or not schemas:
            raise ValueError("at least one tool schema is required")
        if not isinstance(handlers, dict) or set(schemas) != set(handlers):
            raise ValueError("each registered schema must have exactly one handler")

        for name, model in schemas.items():
            if not isinstance(name, str) or not _TOOL_NAME.fullmatch(name):
                raise ValueError("tool names must match [a-z][a-z0-9_]{0,63}")
            if not isinstance(model, type) or not issubclass(model, BaseModel):
                raise ValueError("all schemas must be Pydantic model classes")
            if not callable(handlers[name]):
                raise ValueError("all handlers must be callable")

        # Copy caller-owned dictionaries so later mutation cannot silently
        # replace the schema or handler behind the validation boundary.
        self._schemas = dict(schemas)
        self._handlers = dict(handlers)

    def validate(self, name: str, raw: Any) -> BaseModel:
        if not isinstance(name, str) or name not in self._schemas:
            raise ToolCallRejected("tool is not allowlisted")

        if isinstance(raw, str):
            try:
                raw_bytes = raw.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise ToolCallRejected("arguments are not valid UTF-8") from exc
            if len(raw_bytes) > self._limits.max_argument_bytes:
                raise ToolCallRejected("tool arguments exceed size limit")
            try:
                raw = json.loads(
                    raw,
                    parse_constant=_reject_constant,
                    object_pairs_hook=_reject_duplicate_keys,
                )
            except (json.JSONDecodeError, UnicodeError, ValueError, RecursionError) as exc:
                raise ToolCallRejected("arguments are not valid JSON") from exc

        if not isinstance(raw, dict):
            raise ToolCallRejected("arguments must be a JSON object")

        try:
            encoded = json.dumps(
                raw,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ).encode("utf-8")
        except (TypeError, ValueError, UnicodeEncodeError, RecursionError) as exc:
            raise ToolCallRejected("arguments must contain JSON values only") from exc
        if len(encoded) > self._limits.max_argument_bytes:
            raise ToolCallRejected("tool arguments exceed size limit")

        try:
            return self._schemas[name].model_validate(raw, strict=True)
        except ValidationError as exc:
            # Deliberately omit Pydantic messages and input values. Even
            # validation messages can contain fragments of untrusted input.
            issues = [
                {
                    "path": ".".join(str(part) for part in error["loc"])[:160],
                    "type": error["type"][:80],
                }
                for error in exc.errors()[: self._limits.max_feedback_items]
            ]
            raise ToolCallRejected(
                json.dumps({"validation_errors": issues}, separators=(",", ":"))
            ) from exc

    def execute(self, name: str, raw: Any) -> dict[str, Any]:
        args = self.validate(name, raw)
        try:
            result = self._handlers[name](args)
        except Exception as exc:
            raise ToolHandlerFailed(f"trusted handler failed: {name}") from exc

        try:
            encoded = json.dumps(
                result,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            )
            result_bytes = encoded.encode("utf-8")
        except (TypeError, ValueError, UnicodeEncodeError, RecursionError) as exc:
            raise ToolHandlerFailed("trusted handler returned a non-JSON result") from exc
        if len(result_bytes) > self._limits.max_result_bytes:
            raise ToolHandlerFailed("trusted handler result exceeds size limit")
        return {"ok": True, "result": json.loads(encoded)}

    def validate_and_execute(self, name: str, raw: Any) -> dict[str, Any]:
        """Compatibility method retained for the initial tutorial interface."""
        return self.execute(name, raw)

    def schemas(self) -> dict[str, type[BaseModel]]:
        """Return a detached mapping; model classes themselves remain trusted."""
        return dict(self._schemas)
