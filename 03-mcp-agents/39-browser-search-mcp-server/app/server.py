import os
import httpx
from mcp.server.fastmcp import FastMCP
from app.search import normalize_results, validate_query

endpoint = os.getenv("SEARCH_API_URL", "https://api.search.example/v1/search")
token = os.getenv("SEARCH_API_TOKEN", "")
mcp = FastMCP("browser-search")


@mcp.tool()
async def search_web(query: str, limit: int = 10) -> list[dict]:
    """Search via a configured provider; does not browse arbitrary user-supplied URLs."""
    clean = validate_query(query, limit)
    async with httpx.AsyncClient(timeout=8.0) as client:
        response = await client.get(endpoint, params={"q": clean, "limit": limit},
                                    headers={"Authorization": f"Bearer {token}"} if token else {})
        response.raise_for_status()
        return normalize_results(response.json(), limit)


if __name__ == "__main__":
    mcp.run()
