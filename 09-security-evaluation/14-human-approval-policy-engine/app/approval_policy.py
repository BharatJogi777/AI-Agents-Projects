"""Determine whether a proposed action requires human approval."""

def evaluate_approval(*, action: str, impact: str, policy: dict[str, list[str]]) -> dict[str, object]:
    if not action.strip() or impact not in ("low","medium","high","critical"): raise ValueError("valid action and impact are required")
    approval_impacts=policy.get("require_approval_for",["high","critical"])
    blocked=policy.get("blocked_actions",[])
    if not isinstance(approval_impacts,list) or not isinstance(blocked,list): raise TypeError("policy values must be lists")
    if action in blocked: status="blocked"
    elif impact in approval_impacts: status="approval_required"
    else: status="permitted_by_policy"
    return {"action":action,"impact":impact,"status":status,"may_execute":status=="permitted_by_policy"}
