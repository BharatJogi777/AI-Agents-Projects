from kubernetes import client, config
from mcp.server.fastmcp import FastMCP

from app.inventory import list_pods

config.load_kube_config()  # Use an explicitly configured, least-privilege kubeconfig.
_core = client.CoreV1Api()
mcp = FastMCP("kubernetes-read-only")


@mcp.tool()
def get_pods(namespace: str, limit: int = 100) -> list[dict]:
    """Read pod status in one namespace; no cluster mutations are exposed."""
    return list_pods(_core, namespace, limit)


if __name__ == "__main__":
    mcp.run()
