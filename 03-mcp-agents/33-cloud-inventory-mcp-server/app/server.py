import os

import boto3
from mcp.server.fastmcp import FastMCP

from app.inventory import list_inventory

mcp = FastMCP("cloud-inventory")
_region = os.getenv("AWS_REGION", "us-east-1")
_ec2 = boto3.client("ec2", region_name=_region)


@mcp.tool()
def list_ec2_instances(max_items: int = 100) -> list[dict]:
    """List a bounded, read-only inventory of EC2 instances."""
    return list_inventory(_ec2, _region, max_items)


if __name__ == "__main__":
    mcp.run()
