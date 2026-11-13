"""Represent mobile task intents as permission-aware, reviewable action plans."""
from dataclasses import dataclass

SUPPORTED={"open_screen","create_draft","set_preference","show_notification"}
@dataclass(frozen=True)
class MobileAction:
    action: str
    target: str
    parameters: tuple[tuple[str,str], ...]
    requires_confirmation: bool

def plan_action(action: str, target: str, parameters: dict[str,str] | None = None) -> MobileAction:
    if action not in SUPPORTED:
        raise ValueError("unsupported mobile action")
    if not target.strip():
        raise ValueError("target is required")
    params=parameters or {}
    if any(not isinstance(k,str) or not isinstance(v,str) for k,v in params.items()):
        raise TypeError("parameters must be string pairs")
    # Any state-changing operation is explicitly gated for user confirmation.
    return MobileAction(action,target.strip(),tuple(sorted(params.items())),action!="open_screen")

def authorize_execution(plan: MobileAction, *, user_confirmed: bool, granted_permissions: set[str]) -> bool:
    if plan.target not in granted_permissions:
        return False
    return not plan.requires_confirmation or user_confirmed
