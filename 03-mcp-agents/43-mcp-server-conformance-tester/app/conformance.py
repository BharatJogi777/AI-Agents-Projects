from __future__ import annotations

from typing import Any


async def inspect_session(session: Any) -> dict[str, Any]:
    """Run conservative checks against an already initialized MCP ClientSession."""
    report: dict[str, Any] = {"ping": False, "tools_listed": False, "tool_count": 0, "errors": []}
    try:
        await session.ping()
        report["ping"] = True
    except Exception as exc:
        report["errors"].append(f"ping failed: {type(exc).__name__}")
        return report

    try:
        response = await session.list_tools()
        tools = getattr(response, "tools", None)
        if not isinstance(tools, list):
            raise TypeError("list_tools response has no tools list")
        report["tools_listed"] = True
        report["tool_count"] = len(tools)
        names: set[str] = set()
        for tool in tools:
            name = getattr(tool, "name", None)
            schema = getattr(tool, "inputSchema", None)
            if not isinstance(name, str) or not name:
                report["errors"].append("tool has missing name")
            elif name in names:
                report["errors"].append(f"duplicate tool name: {name}")
            names.add(name)
            if not isinstance(schema, dict) or schema.get("type") != "object":
                report["errors"].append(f"tool {name!r} has no object input schema")
    except Exception as exc:
        report["errors"].append(f"list_tools failed: {type(exc).__name__}")
    report["conformant_for_smoke_checks"] = report["ping"] and report["tools_listed"] and not report["errors"]
    return report
