from mcp.server.fastmcp import FastMCP
from app.tenancy import Principal, TenantRepository

# Demo-only identity. Production identity must come from authenticated transport context.
_demo_principal = Principal("demo-user", "tenant-a", frozenset({"reader"}))
_repo = TenantRepository([
    {"id": "a-1", "tenant_id": "tenant-a", "value": "alpha"},
    {"id": "b-1", "tenant_id": "tenant-b", "value": "bravo"},
])
mcp = FastMCP("multi-tenant-isolation-demo")


@mcp.tool()
def list_my_records(limit: int = 100) -> list[dict]:
    """List records scoped to the authenticated demo tenant."""
    return _repo.list_for(_demo_principal, limit)


if __name__ == "__main__":
    mcp.run()
