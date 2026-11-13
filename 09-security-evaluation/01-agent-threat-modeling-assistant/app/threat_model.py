"""Agent threat modeling assistant: deterministic security evaluation helpers."""

def build_threat_model(*, system_description: str, assets: list[str], entry_points: list[str]):
    if not system_description.strip() or not assets or not entry_points:
        raise ValueError("description, assets, and entry points are required")
    if any(not x.strip() for x in assets + entry_points):
        raise ValueError("assets and entry points must be non-empty")
    threats = []
    for entry in entry_points:
        threats.append({"entry_point": entry, "threat": "Untrusted input influences agent decisions", "control": "Validate and classify input; keep instructions separate from data"})
    threats.extend([
        {"entry_point": "tool boundary", "threat": "Excessive tool authority", "control": "Apply least privilege and per-action authorization"},
        {"entry_point": "memory boundary", "threat": "Sensitive data disclosure or persistence", "control": "Minimize, redact, scope, and expire stored data"},
        {"entry_point": "output boundary", "threat": "Unsafe or unsupported claims", "control": "Validate outputs and require evidence for consequential claims"},
    ])
    return {"system": system_description.strip(), "assets": sorted(set(assets)), "threats": threats}
