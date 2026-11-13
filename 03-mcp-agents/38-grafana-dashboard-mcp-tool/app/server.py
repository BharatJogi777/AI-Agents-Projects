import os
from mcp.server.fastmcp import FastMCP
from app.grafana import GrafanaClient

client = GrafanaClient(os.environ["GRAFANA_URL"], os.environ["GRAFANA_API_TOKEN"])
mcp = FastMCP("grafana-dashboard")


@mcp.tool()
async def search_dashboards(query: str = "", limit: int = 50) -> list[dict]:
    """Search dashboard titles and metadata; no dashboard mutation is exposed."""
    return await client.search_dashboards(query, limit)


if __name__ == "__main__":
    mcp.run()
