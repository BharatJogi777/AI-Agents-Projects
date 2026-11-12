"""Strict argument schemas and deterministic local tool implementations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    a: float = Field(allow_inf_nan=False, ge=-1e12, le=1e12)
    b: float = Field(allow_inf_nan=False, ge=-1e12, le=1e12)


class TextArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    text: str = Field(min_length=1, max_length=2000)


class TimeArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    timezone: str = Field(default="UTC", min_length=1, max_length=64)

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError("timezone must be a valid IANA timezone") from None
        return value


class EmptyArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


ToolEntry = tuple[type[BaseModel], Callable[[BaseModel], dict], str]


def _add(args: AddArgs) -> dict:
    return {"sum": args.a + args.b}


def _text_length(args: TextArgs) -> dict:
    return {"length": len(args.text), "utf8_bytes": len(args.text.encode("utf-8"))}


def _current_time(args: TimeArgs) -> dict:
    now = datetime.now(timezone.utc).astimezone(ZoneInfo(args.timezone))
    return {"timezone": args.timezone, "iso8601": now.isoformat()}


def build_tool_registry() -> dict[str, ToolEntry]:
    """Return a fresh allowlist; model output cannot register or execute code."""
    return {
        "add_numbers": (
            AddArgs,
            _add,
            "Add two finite numbers within the supported range.",
        ),
        "text_length": (
            TextArgs,
            _text_length,
            "Count Unicode code points and UTF-8 bytes in text.",
        ),
        "current_time": (
            TimeArgs,
            _current_time,
            "Return the current time in a supplied IANA timezone; defaults to UTC.",
        ),
    }


def tool_definitions(registry: dict[str, ToolEntry]) -> list[dict]:
    """Convert the allowlist into Ollama's function-tool schema format."""
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": schema.model_json_schema(),
            },
        }
        for name, (schema, _handler, description) in registry.items()
    ]
