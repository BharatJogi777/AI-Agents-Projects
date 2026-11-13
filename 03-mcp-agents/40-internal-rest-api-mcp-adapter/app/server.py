import os
import httpx
from mcp.server.fastmcp import FastMCP
from app.adapter import RestAdapter

adapter = RestAdapter(os.environ["INTERNAL_API_URL"], os.getenv("INTERNAL_API_TOKEN", ""),
                      {"/v1/services", "/v1/deployments"})
mcp = FastMCP("internal-rest-adapter")


@mcp.tool()
async def get_services() -> dict:
    """Read the allowlisted service inventory."""
    return await adapter.get("/v1/services")


@mcp.tool()
async def get_deployments() -> dict:
    """Read the allowlisted deployment inventory."""
    return await adapter.get("/v1/deployments")


if __name__ == "__main__":
    mcp.run()
