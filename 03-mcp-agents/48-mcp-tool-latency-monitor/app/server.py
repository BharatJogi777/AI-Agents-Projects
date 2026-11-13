from mcp.server.fastmcp import FastMCP
from app.monitor import LatencyMonitor

mcp = FastMCP("tool-latency-monitor")
monitor = LatencyMonitor()


@mcp.tool()
def latency_summary(tool: str) -> dict[str, int | float | str]:
    """Return aggregate latency metrics for a previously observed tool."""
    result = monitor.summary(tool)
    return result.__dict__


if __name__ == "__main__":
    mcp.run()
