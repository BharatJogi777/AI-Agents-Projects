"""Offline security checks for Kubernetes workload manifests."""
from typing import Any

def review_manifests(manifests: list[dict[str, Any]]) -> list[dict[str, str]]:
    findings = []
    for index, doc in enumerate(manifests):
        if not isinstance(doc, dict) or not doc.get("kind"):
            raise ValueError(f"manifest {index}: expected an object with kind")
        kind = doc["kind"]
        metadata = doc.get("metadata") or {}
        spec = doc.get("spec") or {}
        pod = spec.get("template", {}).get("spec", {}) if kind in {"Deployment","StatefulSet","DaemonSet","Job","CronJob"} else spec
        if kind == "CronJob":
            pod = spec.get("jobTemplate", {}).get("spec", {}).get("template", {}).get("spec", {})
        if not isinstance(pod, dict):
            continue
        security_context = pod.get("securityContext") or {}
        if security_context.get("runAsNonRoot") is not True:
            findings.append({"severity":"medium","code":"RUN_AS_NON_ROOT","resource":metadata.get("name","unknown"),"message":"Set pod securityContext.runAsNonRoot: true where compatible."})
        if security_context.get("seccompProfile", {}).get("type") not in {"RuntimeDefault","Localhost"}:
            findings.append({"severity":"medium","code":"SECCOMP_PROFILE","resource":metadata.get("name","unknown"),"message":"Set an explicit RuntimeDefault or approved Localhost seccomp profile."})
        for container in pod.get("containers", []) + pod.get("initContainers", []):
            name = container.get("name", "unnamed")
            security = container.get("securityContext") or {}
            if security.get("privileged") is True:
                findings.append({"severity":"critical","code":"PRIVILEGED","resource":metadata.get("name","unknown"),"message":f"{name}: privileged container access is enabled."})
            if security.get("allowPrivilegeEscalation") is not False:
                findings.append({"severity":"high","code":"PRIVILEGE_ESCALATION","resource":metadata.get("name","unknown"),"message":f"{name}: explicitly disable privilege escalation."})
            if security.get("readOnlyRootFilesystem") is not True:
                findings.append({"severity":"low","code":"WRITABLE_ROOT","resource":metadata.get("name","unknown"),"message":f"{name}: consider a read-only root filesystem and explicit writable volumes."})
            dropped = security.get("capabilities", {}).get("drop", [])
            if "ALL" not in dropped:
                findings.append({"severity":"medium","code":"CAPABILITIES_NOT_DROPPED","resource":metadata.get("name","unknown"),"message":f"{name}: drop all Linux capabilities and add back only what is required."})
            if security.get("runAsUser") == 0:
                findings.append({"severity":"high","code":"ROOT_USER","resource":metadata.get("name","unknown"),"message":f"{name}: container explicitly runs as UID 0."})
        if pod.get("hostNetwork") is True:
            findings.append({"severity":"high","code":"HOST_NETWORK","resource":metadata.get("name","unknown"),"message":"hostNetwork shares the node network namespace; verify necessity."})
        if pod.get("hostPID") is True or pod.get("hostIPC") is True:
            findings.append({"severity":"high","code":"HOST_NAMESPACE","resource":metadata.get("name","unknown"),"message":"Host PID/IPC namespaces increase cross-workload exposure."})
    return findings
