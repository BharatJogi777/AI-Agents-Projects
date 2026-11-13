from mcp.server.fastmcp import FastMCP
from app.contracts import validate_arguments, validate_tool_contract
mcp = FastMCP("mcp-tool-contract-harness")

@mcp.tool()
def inspect_tool_contract(tool: dict) -> list[str]:
    """Return contract definition errors without executing the tool."""
    return validate_tool_contract(tool)

@mcp.tool()
def inspect_arguments(schema: dict, arguments: dict) -> list[str]:
    """Validate arguments against a JSON Schema."""
    return validate_arguments(schema, arguments)

if __name__ == "__main__":
    mcp.run()
