import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from app.generator import generate_tool_specs
mcp = FastMCP("openapi-tool-spec-generator")

@mcp.tool()
def generate_specs(openapi_path: str) -> list[dict]:
    """Read a local JSON OpenAPI document and emit GET-only descriptors."""
    path = Path(openapi_path).resolve()
    if path.suffix.lower() != ".json" or not path.is_file() or path.stat().st_size > 2_000_000:
        raise ValueError("provide an existing JSON file no larger than 2 MB")
    return generate_tool_specs(json.loads(path.read_text(encoding="utf-8")))

if __name__ == "__main__":
    mcp.run()
