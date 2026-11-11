"""Typed schemas and deterministic implementations for the tool allowlist."""

from datetime import datetime, timezone
from typing import Callable

from pydantic import BaseModel, ConfigDict, Field


class AddArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    a: float = Field(allow_inf_nan=False, ge=-1e12, le=1e12)
    b: float = Field(allow_inf_nan=False, ge=-1e12, le=1e12)


class TextArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    text: str = Field(min_length=1, max_length=2000)


class EmptyArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


def build_tool_registry() -> dict:
    """Return fresh registry entries; handlers are local, deterministic Python."""
    return {
        "add_numbers": (
            AddArgs,
            lambda args: {"sum": args.a + args.b},
            "Add two finite numbers within the supported range.",
        ),
        "text_length": (
            TextArgs,
            lambda args: {"length": len(args.text)},
            "Count Unicode code points in the supplied text.",
        ),
        "current_utc_time": (
            EmptyArgs,
            lambda _args: {"utc": datetime.now(timezone.utc).isoformat()},
            "Return the current UTC time.",
        ),
    }


def tool_definitions(registry: dict) -> list[dict]:
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
