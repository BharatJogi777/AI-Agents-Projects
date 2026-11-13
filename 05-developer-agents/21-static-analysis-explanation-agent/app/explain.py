"""Turn scanner findings into consistent, evidence-preserving explanations."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Explanation:
    rule_id: str
    severity: str
    location: str
    summary: str
    impact: str
    evidence: str
    verification_steps: tuple[str, ...]


def explain_findings(findings: list[dict]) -> list[Explanation]:
    if not isinstance(findings, list):
        raise TypeError("findings must be a list")
    output = []
    for item in findings:
        if not isinstance(item, dict):
            raise ValueError("each finding must be a mapping")
        required = ("rule_id", "severity", "location", "message")
        if any(not isinstance(item.get(key), str) or not item[key].strip() for key in required):
            raise ValueError(f"finding requires non-empty fields: {', '.join(required)}")
        severity = item["severity"].lower()
        if severity not in ("critical", "high", "medium", "low", "info"):
            raise ValueError("unsupported severity")
        evidence = item.get("evidence", "")
        if not isinstance(evidence, str):
            raise ValueError("evidence must be text")
        impact = {
            "critical": "Potentially severe impact; validate exposure and containment immediately",
            "high": "Potential significant impact; prioritize validation and remediation",
            "medium": "Potential moderate impact; confirm exploitability and affected paths",
            "low": "Potential limited impact; verify context and project policy",
            "info": "Informational observation; determine whether action is warranted",
        }[severity]
        output.append(Explanation(item["rule_id"], severity, item["location"], item["message"],
                                  impact, evidence, ("Inspect the referenced code and surrounding control flow",
                                  "Reproduce or construct a focused test", "Confirm the fix removes the condition without regression")))
    return output


def to_json(items: list[Explanation]) -> str:
    return json.dumps([asdict(x) for x in items], indent=2)


if __name__ == "__main__":
    print(to_json(explain_findings([{"rule_id": "S001", "severity": "high", "location": "app.py:10", "message": "Unsafe input"}])))
