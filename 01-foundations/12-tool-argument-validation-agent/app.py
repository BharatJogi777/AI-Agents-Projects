"""Backward-compatible facade. New code should import from tool_gate."""
from pydantic import BaseModel, ConfigDict

from tool_gate import ArgumentGate, ToolCallRejected, ToolHandlerFailed


class SearchArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    query: str
    limit: int


def demo_search(args: SearchArgs) -> dict:
    if not args.query.strip():
        raise ValueError("query cannot be blank")
    if not 1 <= args.limit <= 20:
        raise ValueError("limit must be 1..20")
    return {"query": args.query, "limit": args.limit, "items": []}


def build_demo_gate() -> ArgumentGate:
    return ArgumentGate({"search": SearchArgs}, {"search": demo_search})


__all__ = ["ArgumentGate", "ToolCallRejected", "ToolHandlerFailed",
           "SearchArgs", "demo_search", "build_demo_gate"]
