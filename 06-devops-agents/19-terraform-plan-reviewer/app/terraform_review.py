"""Review Terraform plan JSON; never apply or approve changes."""
from typing import Any

def review_plan(plan: dict[str, Any]) -> list[dict[str, str]]:
    if not isinstance(plan,dict) or not isinstance(plan.get("resource_changes"),list):
        raise ValueError("plan.resource_changes must be a list")
    findings=[]
    for item in plan["resource_changes"]:
        address=item.get("address")
        change=item.get("change") or {}
        actions=change.get("actions") or []
        if not address or not isinstance(actions,list):
            raise ValueError("each resource change requires address and actions")
        if "delete" in actions:
            findings.append({"severity":"high","code":"RESOURCE_DELETE","resource":address,"message":"Plan includes resource deletion; verify data retention, dependencies, and recovery."})
        if actions == ["delete","create"]:
            findings.append({"severity":"high","code":"REPLACEMENT","resource":address,"message":"Resource replacement may cause downtime or data loss; inspect lifecycle and migration strategy."})
        after=change.get("after") or {}
        if after.get("publicly_accessible") is True or after.get("public") is True:
            findings.append({"severity":"high","code":"PUBLIC_EXPOSURE","resource":address,"message":"Planned configuration exposes a resource publicly; verify explicit business need and network controls."})
        if after.get("privileged") is True or after.get("admin") is True:
            findings.append({"severity":"high","code":"PRIVILEGE_EXPANSION","resource":address,"message":"Planned configuration enables elevated privileges; review least-privilege scope."})
    return findings
