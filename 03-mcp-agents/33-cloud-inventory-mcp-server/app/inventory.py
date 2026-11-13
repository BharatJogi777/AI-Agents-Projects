from __future__ import annotations

from typing import Any


def summarize_instance(instance: dict[str, Any]) -> dict[str, Any]:
    """Return a safe, stable subset of an EC2 instance description."""
    instance_id = instance.get("InstanceId")
    state = (instance.get("State") or {}).get("Name")
    if not isinstance(instance_id, str) or not instance_id:
        raise ValueError("instance is missing InstanceId")
    if not isinstance(state, str):
        raise ValueError("instance is missing state")
    return {
        "instance_id": instance_id,
        "state": state,
        "instance_type": instance.get("InstanceType"),
        "availability_zone": (instance.get("Placement") or {}).get("AvailabilityZone"),
        "private_ip": instance.get("PrivateIpAddress"),
        "tags": [
            {"key": t["Key"], "value": t["Value"]}
            for t in instance.get("Tags", [])
            if isinstance(t, dict) and isinstance(t.get("Key"), str) and isinstance(t.get("Value"), str)
        ],
    }


def list_inventory(ec2_client: Any, region: str, max_items: int = 100) -> list[dict[str, Any]]:
    if not region or not 1 <= max_items <= 500:
        raise ValueError("region is required and max_items must be between 1 and 500")
    paginator = ec2_client.get_paginator("describe_instances")
    output: list[dict[str, Any]] = []
    for page in paginator.paginate(PaginationConfig={"MaxItems": max_items}):
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                output.append(summarize_instance(instance))
                if len(output) >= max_items:
                    return output
    return output
