"""Explain differences between desired and observed resource state."""
from typing import Any

def explain_drift(desired: dict[str, Any], observed: dict[str, Any], sensitive_keys: set[str] | None = None) -> list[dict[str, Any]]:
    if not isinstance(desired,dict) or not isinstance(observed,dict):
        raise ValueError("desired and observed states must be mappings")
    sensitive_keys=sensitive_keys or {"password","secret","token","private_key","access_key"}
    findings=[]
    def walk(path: str, left: Any, right: Any) -> None:
        if isinstance(left,dict) and isinstance(right,dict):
            for key in sorted(set(left)|set(right)):
                walk(f"{path}.{key}" if path else key,left.get(key,"<missing>"),right.get(key,"<missing>"))
        elif left != right:
            key=path.rsplit(".",1)[-1].lower()
            secret=any(marker in key for marker in sensitive_keys)
            findings.append({"path":path,"desired":"[REDACTED]" if secret else left,"observed":"[REDACTED]" if secret else right,"sensitive":secret,"change":"added" if left=="<missing>" else "removed" if right=="<missing>" else "modified"})
    walk("",desired,observed)
    return findings
