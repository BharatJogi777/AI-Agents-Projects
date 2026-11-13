"""Recommend Kubernetes requests from observed utilization."""
from statistics import median
from typing import Any

def advise_resources(samples: list[dict[str, Any]], headroom: float = 1.25) -> list[dict[str, Any]]:
    if not isinstance(headroom, (int, float)) or not 1.0 <= headroom <= 2.0:
        raise ValueError("headroom must be between 1.0 and 2.0")
    grouped: dict[tuple[str, str], list[dict]] = {}
    for i, row in enumerate(samples):
        for key in ("namespace", "pod", "container", "cpu_millicores", "memory_mib", "cpu_request_millicores", "memory_request_mib"):
            if key not in row:
                raise ValueError(f"sample {i}: missing {key}")
        numeric = [row[k] for k in ("cpu_millicores","memory_mib","cpu_request_millicores","memory_request_mib")]
        if any(not isinstance(v, (int, float)) or v < 0 for v in numeric):
            raise ValueError(f"sample {i}: resource values must be non-negative numbers")
        grouped.setdefault((row["namespace"], row["container"]), []).append(row)
    output = []
    for (namespace, container), rows in grouped.items():
        cpu = median(r["cpu_millicores"] for r in rows)
        mem = median(r["memory_mib"] for r in rows)
        cpu_req = max(r["cpu_request_millicores"] for r in rows)
        mem_req = max(r["memory_request_mib"] for r in rows)
        output.append({
            "namespace": namespace, "container": container, "sample_count": len(rows),
            "median_cpu_millicores": cpu, "median_memory_mib": mem,
            "suggested_cpu_request_millicores": int(round(cpu * headroom)),
            "suggested_memory_request_mib": int(round(mem * headroom)),
            "cpu_request_utilization_pct": round(cpu / cpu_req * 100, 1) if cpu_req else None,
            "memory_request_utilization_pct": round(mem / mem_req * 100, 1) if mem_req else None,
            "note": "Recommendation only; validate peak, startup, and seasonal usage before changing manifests."
        })
    return sorted(output, key=lambda x: (x["namespace"], x["container"]))
