from mcp.server.fastmcp import FastMCP

mcp = FastMCP("deployment-template")


@mcp.tool()
def readiness() -> dict[str, str]:
    """Return static process readiness information."""
    return {"status": "ready", "transport": "stdio"}


if __name__ == "__main__":
    mcp.run()
