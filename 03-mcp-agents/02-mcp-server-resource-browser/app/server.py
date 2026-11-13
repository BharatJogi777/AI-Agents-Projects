"""MCP stdio server exposing read-only order resources."""
from mcp.server.fastmcp import FastMCP

from app.services.order_resources import OrderResourceService

mcp = FastMCP("order-resource-browser")
resources = OrderResourceService()


@mcp.resource("orders://{order_id}", mime_type="application/json")
def read_order(order_id: str) -> str:
    """Read a sample order by its stable order identifier."""
    return resources.read(order_id)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
