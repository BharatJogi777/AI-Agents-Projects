"""Inventory declared software licenses and flag policy conflicts."""
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass(frozen=True)
class Finding:
    package: str
    license: str
    severity: str
    reason: str

DEFAULT_POLICY = {"allowed": {"MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "ISC"}, "review": {"MPL-2.0", "LGPL-2.1", "LGPL-3.0"}, "denied": {"GPL-2.0", "GPL-3.0", "AGPL-3.0"}}

def audit(records: list[dict], policy: dict | None = None) -> list[Finding]:
    policy = policy or DEFAULT_POLICY
    seen=set(); findings=[]
    for row in records:
        if not isinstance(row, dict) or not row.get("name") or not row.get("license"):
            raise ValueError("Each record requires name and license")
        name, lic=str(row["name"]).strip(), str(row["license"]).strip()
        if not name or not lic: raise ValueError("Package name and license cannot be blank")
        key=(name.lower(),lic)
        if key in seen: continue
        seen.add(key)
        if lic in policy["denied"]: findings.append(Finding(name,lic,"high","License is denied by policy"))
        elif lic in policy["review"]: findings.append(Finding(name,lic,"medium","Legal review required by policy"))
        elif lic not in policy["allowed"]: findings.append(Finding(name,lic,"unknown","License is not covered by policy"))
    return findings

def parse_requirements(path: str | Path) -> list[dict]:
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith(("#","-")): continue
        match=re.match(r"([A-Za-z0-9_.-]+)",line)
        if match: rows.append({"name":match.group(1),"license":"UNKNOWN"})
    return rows
