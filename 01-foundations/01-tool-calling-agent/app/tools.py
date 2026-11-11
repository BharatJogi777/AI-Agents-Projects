from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class AddArguments(BaseModel):
    a: float = Field(description="First number")
    b: float = Field(description="Second number")


def add_numbers(arguments: dict[str, Any]) -> dict[str, float]:
    parsed = AddArguments.model_validate(arguments)
    return {"result": parsed.a + parsed.b}


def get_current_utc_time(arguments: dict[str, Any]) -> dict[str, str]:
    if arguments:
        raise ValueError("get_current_utc_time accepts no arguments")
    return {"utc_time": datetime.now(timezone.utc).isoformat()}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers. Use this for arithmetic addition.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_utc_time",
            "description": "Return the current UTC time. This tool takes no arguments.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]

_TOOL_HANDLERS = {
    "add_numbers": add_numbers,
    "get_current_utc_time": get_current_utc_time,
}


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    handler = _TOOL_HANDLERS.get(name)
    if handler is None:
        raise ValueError(f"Tool is not allowlisted: {name}")
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be a JSON object")
    try:
        return handler(arguments)
    except ValidationError as exc:
        raise ValueError(f"Invalid arguments for {name}: {exc}") from exc
