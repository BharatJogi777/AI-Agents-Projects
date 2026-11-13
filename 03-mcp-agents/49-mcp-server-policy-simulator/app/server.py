from mcp.server.fastmcp import FastMCP
from app.policy import AccessRequest, PolicyEngine, PolicyRule

mcp = FastMCP("policy-simulator")
policy = PolicyEngine([
    PolicyRule(frozenset({"demo-user"}), frozenset({"read_status"}), frozenset({"status:read"}))
])


@mcp.tool()
def read_status(principal: str, scope: str = "status:read") -> dict[str, str | bool]:
    """Read a harmless demo status after deterministic policy evaluation."""
    decision = policy.evaluate(AccessRequest(principal, "read_status", frozenset({scope})))
    if not decision.allowed:
        return {"allowed": False, "reason": decision.reason}
    return {"allowed": True, "status": "healthy"}


if __name__ == "__main__":
    mcp.run()
