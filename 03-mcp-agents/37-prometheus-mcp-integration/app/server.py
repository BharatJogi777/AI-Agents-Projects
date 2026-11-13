import os

import httpx
from mcp.server.fastmcp import FastMCP

from app.prometheus import normalize_result, validate_promql

_url = os.getenv("PROMETHEUS_URL", "http://localhost:9090").rstrip("/")
mcp = FastMCP("prometheus-integration")


@mcp.tool()
async def instant_query(query: str) -> list[dict]:
    """Execute a PromQL instant query and return at most 500 series."""
    expression = validate_promql(query)
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(f"{_url}/api/v1/query", params={"query": expression})
        response.raise_for_status()
        return normalize_result(response.json())


if __name__ == "__main__":
    mcp.run()
