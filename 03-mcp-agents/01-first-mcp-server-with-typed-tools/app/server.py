"""MCP transport adapter. Business rules live in app.domain.orders."""

from mcp.server.fastmcp import FastMCP

from app.domain.orders import calculate_order_total, get_order_status

mcp = FastMCP(
    name="orders-demo",
    instructions=(
        "Read-only order status lookup and deterministic order total calculation. "
        "These tools use sample data and do not access a real order system."
    ),
)


@mcp.tool()
def calculate_order_total_tool(
    quantity: int,
    unit_price: float,
    tax_rate: float = 0.18,
) -> dict[str, int | str]:
    """Calculate subtotal, tax, and total for a quantity at a unit price."""
    return calculate_order_total(quantity, unit_price, tax_rate).as_dict()


@mcp.tool()
def get_order_status_tool(order_id: str) -> dict[str, str]:
    """Look up the status of a sample order such as ORD-1001."""
    return get_order_status(order_id)


def main() -> None:
    """Start the stdio MCP server for an MCP host to launch."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
