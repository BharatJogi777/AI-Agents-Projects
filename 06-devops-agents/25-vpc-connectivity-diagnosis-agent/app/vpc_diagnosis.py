"""Explain likely blockers in an explicitly supplied VPC path snapshot."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Diagnostic:
    component: str
    status: str
    explanation: str
    next_check: str

def diagnose_path(path: dict) -> list[Diagnostic]:
    if not isinstance(path, dict): raise TypeError("path must be an object")
    required = ("route", "security_group", "network_acl", "endpoint")
    missing = [key for key in required if key not in path]
    if missing: raise ValueError("missing path components: " + ", ".join(missing))
    results = []
    checks = {
        "route": ("Route table", "Verify destination prefix, target, and target health."),
        "security_group": ("Security group", "Verify source/destination rules and protocol/port."),
        "network_acl": ("Network ACL", "Verify inbound and outbound rules, including ephemeral return ports."),
        "endpoint": ("Endpoint", "Verify endpoint state, private DNS, policy, and service association."),
    }
    for key in required:
        value = path[key]
        if not isinstance(value, dict) or not isinstance(value.get("reachable"), bool):
            raise ValueError(f"{key}.reachable must be a boolean")
        component, next_check = checks[key]
        if not value["reachable"]:
            results.append(Diagnostic(component, "blocked", str(value.get("evidence", "No supporting evidence supplied.")), next_check))
        else:
            results.append(Diagnostic(component, "passed", str(value.get("evidence", "Marked reachable in supplied snapshot.")), next_check))
    return results
