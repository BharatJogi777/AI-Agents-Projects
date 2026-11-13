"""Represent accessible browser actions as reviewable, user-approved steps."""
from dataclasses import dataclass
@dataclass(frozen=True)
class UIAction:
    role:str
    accessible_name:str
    operation:str
    target_url:str
def validate_action(a:UIAction,allowed_operations:set[str],allowed_hosts:set[str])->UIAction:
    from urllib.parse import urlsplit
    p=urlsplit(a.target_url)
    if not a.role.strip() or not a.accessible_name.strip(): raise ValueError("role and accessible name are required")
    if a.operation not in allowed_operations: raise ValueError("operation is not allowlisted")
    if p.scheme!="https" or p.hostname not in allowed_hosts: raise ValueError("target host is not allowlisted HTTPS")
    return a
def prepare_action_plan(actions:list[UIAction],allowed_operations:set[str],allowed_hosts:set[str])->dict:
    if not actions: raise ValueError("at least one action is required")
    checked=[validate_action(a,allowed_operations,allowed_hosts) for a in actions]
    return {"steps":[a.__dict__ for a in checked],"requires_user_confirmation":True,"executed":False}
