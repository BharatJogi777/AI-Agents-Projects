"""Static review of IAM-style policy documents; not a substitute for cloud policy simulation."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class PolicyFinding:
    severity: str
    statement_index: int
    issue: str
    evidence: str

def _values(value: Any) -> list[str]:
    if isinstance(value, str): return [value]
    if isinstance(value, list) and all(isinstance(x, str) for x in value): return value
    raise ValueError("policy action/resource must be a string or list of strings")

def review_policy(policy: dict[str, Any]) -> list[PolicyFinding]:
    if not isinstance(policy, dict): raise TypeError("policy must be an object")
    statements = policy.get("Statement")
    if isinstance(statements, dict): statements = [statements]
    if not isinstance(statements, list): raise ValueError("Statement must be an object or list")
    findings = []
    for i, statement in enumerate(statements):
        if not isinstance(statement, dict): raise ValueError(f"statement {i} must be an object")
        effect = statement.get("Effect")
        if effect not in {"Allow", "Deny"}: raise ValueError(f"statement {i} has invalid Effect")
        actions = _values(statement.get("Action", []))
        resources = _values(statement.get("Resource", []))
        if effect == "Allow" and any(a == "*" for a in actions):
            findings.append(PolicyFinding("critical", i, "Wildcard action", "Action includes *"))
        if effect == "Allow" and any(r == "*" for r in resources):
            findings.append(PolicyFinding("high", i, "Wildcard resource", "Resource includes *"))
        risky = [a for a in actions if a.endswith(":PutRolePolicy") or a.endswith(":AttachRolePolicy") or a.endswith(":CreateAccessKey")]
        if effect == "Allow" and risky:
            findings.append(PolicyFinding("high", i, "Privilege-management action", ", ".join(risky)))
    return findings
