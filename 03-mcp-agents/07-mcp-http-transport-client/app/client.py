"""Streamable HTTP MCP client."""
from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from app.config import ClientConfig


async def run_client(*, tool_name: str | None = None, arguments: dict[str, Any] | None = None) -> Any:
    config = ClientConfig.from_env()
    headers = {"Authorization": f"Bearer {config.bearer_token}"} if config.bearer_token else None
    async with streamablehttp_client(config.server_url, headers=headers) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            if tool_name is None:
                result = await session.list_tools()
                return [{"name": tool.name, "description": tool.description} for tool in result.tools]
            return await session.call_tool(tool_name, arguments or {})


def parse_payload(raw: str) -> dict[str, Any]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("arguments must decode to a JSON object")
    return value


async def main() -> None:
    parser = argparse.ArgumentParser(description="MCP Streamable HTTP client")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--tool")
    parser.add_argument("--arguments", default="{}")
    args = parser.parse_args()
    try:
        payload = parse_payload(args.arguments)
    except (json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"--arguments must be a JSON object: {exc}") from exc
    print(await run_client(tool_name=args.tool if not args.list else None, arguments=payload))


if __name__ == "__main__":
    asyncio.run(main())
