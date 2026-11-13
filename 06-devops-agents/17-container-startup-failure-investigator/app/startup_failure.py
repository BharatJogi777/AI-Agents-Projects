"""Classify container startup failures from supplied evidence."""
from typing import Any

def investigate_startup(container: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(container, dict):
        raise ValueError("container must be an object")
    for key in ("name","state"):
        if not container.get(key):
            raise ValueError(f"{key} is required")
    state = str(container["state"]).lower()
    code = container.get("exit_code")
    reason = str(container.get("reason", ""))
    logs = str(container.get("logs", ""))
    if code is not None and (not isinstance(code, int) or code < 0):
        raise ValueError("exit_code must be a non-negative integer or null")
    rules = [
        (state in {"imagepullbackoff","errimagepull"} or "pull access denied" in logs.lower(), "IMAGE_PULL", "Check image name, tag, registry credentials, and network access."),
        (code == 137 or "oomkilled" in reason.lower(), "OUT_OF_MEMORY", "Inspect memory limits and peak usage; determine whether the process exceeded its cgroup limit."),
        (code == 126 or "permission denied" in logs.lower(), "EXEC_PERMISSION", "Check entrypoint permissions, executable format, and mounted volume permissions."),
        (code == 127 or "executable file not found" in logs.lower(), "COMMAND_NOT_FOUND", "Verify the image entrypoint, command override, and executable path."),
        (code == 1 or state in {"exited","crashloopbackoff"}, "APPLICATION_EXIT", "Inspect complete application logs, required environment, configuration, and dependency readiness."),
    ]
    for matched, category, action in rules:
        if matched:
            return {"container":container["name"],"category":category,"evidence":{"state":state,"exit_code":code,"reason":reason},"next_checks":[action],"confidence":"heuristic"}
    return {"container":container["name"],"category":"INSUFFICIENT_EVIDENCE","evidence":{"state":state,"exit_code":code,"reason":reason},"next_checks":["Collect full startup logs, inspect runtime events, and verify image entrypoint and configuration."],"confidence":"low"}
