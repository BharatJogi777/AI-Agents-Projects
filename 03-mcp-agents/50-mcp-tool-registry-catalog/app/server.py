from mcp.server.fastmcp import FastMCP
from app.registry import ToolRecord, ToolRegistry

mcp = FastMCP("tool-registry-catalog")
registry = ToolRegistry()
registry.register(ToolRecord(
    server="example", name="get_health", description="Read example health",
    version="1.0.0", input_schema={"type": "object", "properties": {}, "required": []},
))


@mcp.tool()
def list_tools(server: str | None = None) -> list[dict]:
    """List registered tool metadata; this does not invoke any tool."""
    return [
        {"server": item["server"], "name": item["name"], "description": item["description"],
         "version": item["version"], "input_schema": item["input_schema"]}
        for item in registry.export()
        if server is None or item["server"] == server
    ]


if __name__ == "__main__":
    mcp.run()
