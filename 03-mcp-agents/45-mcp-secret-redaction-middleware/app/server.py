from mcp.server.fastmcp import FastMCP
from app.redaction import redact

mcp = FastMCP("secret-redaction-demo")


@mcp.tool()
def sanitize_diagnostic_payload(payload: dict) -> dict:
    """Return a redacted copy of a diagnostic object; never mutates input."""
    return redact(payload)


if __name__ == "__main__":
    mcp.run()
