import docker
from mcp.server.fastmcp import FastMCP

from app.inventory import list_containers

_client = docker.from_env()
mcp = FastMCP("docker-inspection")


@mcp.tool()
def inspect_containers(all_containers: bool = False, limit: int = 100) -> list[dict]:
    """Inspect container metadata; this server does not start, stop, or exec containers."""
    return list_containers(_client, all_containers, limit)


if __name__ == "__main__":
    mcp.run()
