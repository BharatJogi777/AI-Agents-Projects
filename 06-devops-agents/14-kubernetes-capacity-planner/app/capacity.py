"""Plan Kubernetes node capacity from workload requests."""
from math import ceil
from typing import Any

def plan_capacity(workloads: list[dict[str, Any]], node_capacity: dict[str, float], reserve: float = 0.15) -> dict[str, Any]:
    if not 0 <= reserve < 0.8:
        raise ValueError("reserve must be in [0, 0.8)")
    for resource in ("cpu_millicores", "memory_mib"):
        if resource not in node_capacity or not isinstance(node_capacity[resource], (int, float)) or node_capacity[resource] <= 0:
            raise ValueError(f"node_capacity.{resource} must be positive")
    totals = {"cpu_millicores": 0.0, "memory_mib": 0.0}
    for i, workload in enumerate(workloads):
        for resource in totals:
            value = workload.get(resource)
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"workload {i}: {resource} must be a non-negative number")
            totals[resource] += value
    usable = {key: value * (1 - reserve) for key, value in node_capacity.items()}
    cpu_nodes = ceil(totals["cpu_millicores"] / usable["cpu_millicores"])
    mem_nodes = ceil(totals["memory_mib"] / usable["memory_mib"])
    count = max(cpu_nodes, mem_nodes, 1 if workloads else 0)
    return {
        "workload_totals": totals, "usable_per_node": usable,
        "nodes_required": count, "limiting_resource": "cpu" if cpu_nodes >= mem_nodes else "memory",
        "cpu_utilization_pct": round(totals["cpu_millicores"] / (count * node_capacity["cpu_millicores"]) * 100, 1) if count else 0,
        "memory_utilization_pct": round(totals["memory_mib"] / (count * node_capacity["memory_mib"]) * 100, 1) if count else 0,
        "assumptions": ["Requests are summed; actual bin-packing, DaemonSets, system reservations, topology, and autoscaler limits are not modeled."]
    }
