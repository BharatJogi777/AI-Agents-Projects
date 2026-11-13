"""Static deployment review; no cluster access or mutation."""
from typing import Any

def review_deployment(manifest: dict[str, Any]) -> list[dict[str, str]]:
    if not isinstance(manifest, dict) or manifest.get("kind") != "Deployment":
        raise ValueError("manifest kind must be Deployment")
    metadata = manifest.get("metadata") or {}
    spec = manifest.get("spec") or {}
    template = (spec.get("template") or {}).get("spec") or {}
    containers = template.get("containers") or []
    if not metadata.get("name") or not containers:
        raise ValueError("deployment requires metadata.name and at least one container")
    findings: list[dict[str, str]] = []
    replicas = spec.get("replicas", 1)
    if not isinstance(replicas, int) or replicas < 0:
        raise ValueError("spec.replicas must be a non-negative integer")
    if replicas < 2:
        findings.append({"severity":"medium","code":"SINGLE_REPLICA","message":"Fewer than two replicas provide no replica-level availability during disruption."})
    strategy = (spec.get("strategy") or {}).get("type", "RollingUpdate")
    if strategy == "Recreate":
        findings.append({"severity":"medium","code":"RECREATE_STRATEGY","message":"Recreate strategy can cause downtime during rollout."})
    for index, container in enumerate(containers):
        name = container.get("name", f"container-{index}")
        if not container.get("image"):
            raise ValueError(f"{name}: image is required")
        if not container.get("resources", {}).get("requests"):
            findings.append({"severity":"medium","code":"MISSING_REQUESTS","message":f"{name}: CPU and memory requests are not configured."})
        if not container.get("resources", {}).get("limits"):
            findings.append({"severity":"low","code":"MISSING_LIMITS","message":f"{name}: resource limits are not configured; assess workload policy before setting them."})
        if not container.get("readinessProbe"):
            findings.append({"severity":"high","code":"MISSING_READINESS","message":f"{name}: no readiness probe; traffic may reach an unready container."})
        if not container.get("livenessProbe"):
            findings.append({"severity":"low","code":"MISSING_LIVENESS","message":f"{name}: no liveness probe; hung processes may remain running."})
        security = container.get("securityContext") or {}
        if security.get("privileged") is True:
            findings.append({"severity":"high","code":"PRIVILEGED_CONTAINER","message":f"{name}: privileged mode substantially expands container permissions."})
        if security.get("allowPrivilegeEscalation") is True:
            findings.append({"severity":"medium","code":"PRIVILEGE_ESCALATION","message":f"{name}: privilege escalation is explicitly allowed."})
    return findings
