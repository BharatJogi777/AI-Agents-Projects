from mcp.server.fastmcp import FastMCP
from app.boundary import wrap_untrusted_tool_result

mcp = FastMCP("prompt-injection-boundary-demo")


@mcp.tool()
def mark_untrusted_result(server: str, tool: str, result: str) -> dict:
    """Label tool output as untrusted data and preserve its provenance."""
    return wrap_untrusted_tool_result(server, tool, result)


if __name__ == "__main__":
    mcp.run()
