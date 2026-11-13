"""Classify proposed actions using explicit risk indicators."""

def classify_action(*, action: str, indicators: list[str]) -> dict[str, object]:
    if not isinstance(action,str) or not action.strip(): raise ValueError("action is required")
    known={"money_transfer":"critical","delete_data":"high","external_publish":"high","permission_change":"high","read_public_data":"low","draft_only":"low"}
    unknown=[x for x in indicators if x not in known]
    if unknown: raise ValueError(f"unknown indicators: {unknown}")
    levels=[known[x] for x in indicators]
    rank={"low":0,"medium":1,"high":2,"critical":3}
    impact=max(levels,key=lambda x:rank[x]) if levels else "medium"
    return {"action":action,"impact":impact,"indicators":list(indicators),"requires_human_review":impact in ("high","critical")}
