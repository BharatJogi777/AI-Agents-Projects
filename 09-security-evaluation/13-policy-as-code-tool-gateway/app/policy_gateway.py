"""Evaluate tool calls against declarative allow/deny policy rules."""

def authorize_tool_call(*, principal: str, tool: str, action: str, policies: list[dict[str, object]]) -> dict[str, object]:
    if not all(isinstance(x,str) and x.strip() for x in (principal,tool,action)): raise ValueError("principal, tool, and action are required")
    decision="deny"; matched=None
    for index, rule in enumerate(policies):
        if not isinstance(rule,dict) or rule.get("effect") not in ("allow","deny"): raise ValueError("policy rule requires allow or deny effect")
        if rule.get("principal") not in (principal,"*") or rule.get("tool") not in (tool,"*") or rule.get("action") not in (action,"*"): continue
        decision=str(rule["effect"]); matched=index
        if decision=="deny": break
    return {"allowed":decision=="allow","decision":decision,"matched_rule":matched,"default_deny":matched is None}
