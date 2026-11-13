from __future__ import annotations

from typing import Any


def container_summary(container: Any) -> dict[str, Any]:
    attrs = container.attrs or {}
    config = attrs.get("Config") or {}
    state = attrs.get("State") or {}
    return {
        "id": container.short_id,
        "name": container.name,
        "image": config.get("Image"),
        "status": state.get("Status", container.status),
        "started_at": state.get("StartedAt"),
    }


def list_containers(docker_client: Any, all_containers: bool = False, limit: int = 100) -> list[dict[str, Any]]:
    if not isinstance(all_containers, bool) or not 1 <= limit <= 500:
        raise ValueError("all_containers must be boolean and limit must be between 1 and 500")
    containers = docker_client.containers.list(all=all_containers, limit=limit)
    return [container_summary(c) for c in containers[:limit]]
