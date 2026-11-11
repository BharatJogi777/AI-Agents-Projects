"""Typed, allowlisted tool contract for the calculator agent."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from calculator_core.arithmetic import MAX_LENGTH, calculate


class CalculateArguments(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    expression: str = Field(min_length=1, max_length=MAX_LENGTH)


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a basic arithmetic expression deterministically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": MAX_LENGTH,
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    }
]


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, str]:
    if name != "calculate":
        raise ValueError(f"Tool is not allowlisted: {name}")
    try:
        args = CalculateArguments.model_validate(arguments)
    except ValidationError as exc:
        raise ValueError("Invalid calculate arguments") from exc
    return {"expression": args.expression, "result": calculate(args.expression)}
