"""Read-only diagnosis from Kubernetes pod status snapshots."""

def diagnose_pod(pod: dict) -> list[dict]:
    if not isinstance(pod, dict): raise TypeError("pod must be an object")
    metadata=pod.get("metadata") or {}; status=pod.get("status") or {}
    if not metadata.get("name"): raise ValueError("metadata.name is required")
    findings=[]; phase=status.get("phase","Unknown")
    if phase in {"Pending","Failed","Unknown"}: findings.append({"reason":phase,"severity":"warning","message":f"Pod phase is {phase}; inspect scheduling and node conditions."})
    for c in status.get("containerStatuses",[]):
        if not isinstance(c,dict): raise ValueError("container status entries must be objects")
        name=c.get("name","unknown"); state=c.get("state") or {}; waiting=state.get("waiting") or {}; terminated=state.get("terminated") or {}
        if waiting:
            reason=waiting.get("reason","Waiting")
            guidance={"CrashLoopBackOff":"Inspect previous container logs, exit code, probes, and recent configuration changes.","ImagePullBackOff":"Verify image name, tag, registry reachability, and pull-secret permissions.","ErrImagePull":"Check registry authentication and image availability."}.get(reason,"Inspect scheduling events and container prerequisites.")
            findings.append({"container":name,"reason":reason,"severity":"warning","message":guidance})
        if terminated and terminated.get("exitCode",0)!=0:
            findings.append({"container":name,"reason":terminated.get("reason","Terminated"),"exit_code":terminated.get("exitCode"),"severity":"error","message":"Inspect container logs and termination details before restarting."})
        if c.get("ready") is False and not waiting and not terminated:
            findings.append({"container":name,"reason":"NotReady","severity":"warning","message":"Review readiness probe configuration and application health."})
    return findings
