"""Launch and interact with a local MCP server over stdio."""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MCP stdio transport demonstration")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="list server tools")
    group.add_argument("--tool", help="name of a tool to invoke")
    parser.add_argument("--arguments", default="{}", help="JSON object passed to the tool")
    return parser.parse_args()


async def run_client(*, tool_name: str | None = None, arguments: dict[str, Any] | None = None) -> Any:
    project_root = Path(__file__).resolve().parents[1]
    server_script = project_root / "app" / "sample_server.py"
    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(server_script)],
        env=None,
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            if tool_name is None:
                response = await session.list_tools()
                return [{"name": item.name, "description": item.description} for item in response.tools]
            response = await session.call_tool(tool_name, arguments or {})
            return response


async def main() -> None:
    args = parse_arguments()
    try:
        payload = json.loads(args.arguments)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--arguments must be valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("--arguments must decode to a JSON object")
    result = await run_client(tool_name=args.tool if not args.list else None, arguments=payload)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
