"""Evaluate a small, provider-neutral cloud security posture snapshot."""
from dataclasses import dataclass

@dataclass(frozen=True)
class PostureFinding:
    control: str
    severity: str
    asset: str
    evidence: str
    recommendation: str

CONTROLS = {
    "storage_public": ("critical", "Storage is publicly accessible", "Disable public access unless explicitly required and approved."),
    "encryption_disabled": ("high", "Encryption at rest is disabled", "Enable encryption and verify key ownership and rotation."),
    "audit_logging_disabled": ("high", "Audit logging is disabled", "Enable centralized audit logging with retention and alerting."),
    "mfa_disabled": ("high", "MFA is not enforced", "Require MFA for human identities and privileged access."),
    "network_admin_open": ("critical", "Administrative network access is unrestricted", "Restrict administrative ingress to approved sources."),
}

def assess_posture(assets: list[dict]) -> list[PostureFinding]:
    if not isinstance(assets, list): raise TypeError("assets must be a list")
    findings = []
    for i, asset in enumerate(assets):
        if not isinstance(asset, dict): raise ValueError(f"asset {i} must be an object")
        name = asset.get("id")
        if not isinstance(name, str) or not name.strip(): raise ValueError(f"asset {i} requires id")
        controls = asset.get("controls", {})
        if not isinstance(controls, dict): raise ValueError(f"asset {name}: controls must be an object")
        for key, value in controls.items():
            if key not in CONTROLS: continue
            if not isinstance(value, bool): raise ValueError(f"asset {name}: {key} must be boolean")
            if value:
                severity, issue, recommendation = CONTROLS[key]
                findings.append(PostureFinding(key, severity, name, issue, recommendation))
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(findings, key=lambda f: (order[f.severity], f.asset, f.control))
