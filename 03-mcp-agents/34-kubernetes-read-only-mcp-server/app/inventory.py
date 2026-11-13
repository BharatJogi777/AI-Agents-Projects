from __future__ import annotations

from typing import Any


def pod_summary(pod: Any) -> dict[str, Any]:
    metadata = pod.metadata
    status = pod.status
    return {
        "name": metadata.name,
        "namespace": metadata.namespace,
        "phase": status.phase,
        "node": getattr(getattr(pod, "spec", None), "node_name", None),
        "restarts": sum(c.restart_count for c in (status.container_statuses or [])),
    }


def list_pods(core_api: Any, namespace: str, limit: int = 100) -> list[dict[str, Any]]:
    if not namespace or not 1 <= limit <= 500:
        raise ValueError("namespace is required and limit must be between 1 and 500")
    response = core_api.list_namespaced_pod(namespace=namespace, limit=limit)
    return [pod_summary(p) for p in response.items[:limit]]
