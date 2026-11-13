"""Evaluate patch inventory against an explicit approved baseline."""
from dataclasses import dataclass

@dataclass(frozen=True)
class PatchFinding:
    asset: str
    package: str
    installed: str | None
    required: str
    status: str

def _version(v):
    if not isinstance(v,str) or not v.strip(): raise ValueError("versions must be non-empty strings")
    parts=v.split(".")
    if any(not p.isdigit() for p in parts): raise ValueError(f"unsupported version format: {v}")
    return tuple(int(p) for p in parts)

def assess_patch_compliance(inventory: list[dict], baseline: dict[str,str]) -> list[PatchFinding]:
    if not isinstance(inventory,list) or not isinstance(baseline,dict) or not baseline: raise ValueError("inventory and non-empty baseline are required")
    required={k:_version(v) for k,v in baseline.items() if isinstance(k,str) and k}
    if len(required)!=len(baseline): raise ValueError("baseline package names must be non-empty strings")
    out=[]; seen=set()
    for i,item in enumerate(inventory):
        if not isinstance(item,dict): raise ValueError(f"inventory item {i} must be an object")
        asset=item.get("asset"); package=item.get("package"); installed=item.get("installed_version")
        if not isinstance(asset,str) or not asset or not isinstance(package,str) or package not in required: raise ValueError(f"inventory item {i} has unknown asset or package")
        key=(asset,package)
        if key in seen: raise ValueError(f"duplicate inventory entry: {key}")
        seen.add(key)
        if installed is None: status="missing"
        else: status="compliant" if _version(installed)>=required[package] else "outdated"
        out.append(PatchFinding(asset,package,installed,baseline[package],status))
    return out
