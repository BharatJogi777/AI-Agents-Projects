"""Default-deny evaluator for agent tool permission requests."""

def check_tool_permissions(*, requests: list[dict[str, str]], grants: dict[str, list[str]]) -> list[dict[str, object]]:
    if not isinstance(grants, dict):
        raise TypeError("grants must be a dictionary")
    decisions = []
    for request in requests:
        if not isinstance(request, dict) or not request.get("principal") or not request.get("tool") or not request.get("action"):
            raise ValueError("each request requires principal, tool, and action")
        allowed = request["action"] in grants.get(request["principal"] + ":" + request["tool"], [])
        decisions.append({"principal": request["principal"], "tool": request["tool"], "action": request["action"], "allowed": allowed, "reason": "explicit grant" if allowed else "no matching explicit grant"})
    return decisions
