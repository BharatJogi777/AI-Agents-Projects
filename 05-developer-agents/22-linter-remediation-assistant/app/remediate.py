"""Suggest cautious remediation steps for common lint rule families."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Remediation:
    rule_id: str
    guidance: str
    review_checks: tuple[str, ...]
    known_risk: str


RULE_GUIDANCE = {
    "F401": ("Remove the unused import only after checking dynamic or side-effect usage", "Import removal can break plugin registration or side effects"),
    "F841": ("Remove the unused local or use it intentionally", "The value may be retained for debugging or an intended side effect"),
    "E501": ("Wrap the expression or extract a well-named helper", "Avoid changing string contents or query formatting"),
    "B904": ("Chain the new exception with 'raise ... from exc' where causal context matters", "Preserve exception semantics and public error contracts"),
    "UP": ("Review the suggested modernization against the supported Python version", "Modern syntax may raise the minimum runtime requirement"),
}


def suggest_remediations(rule_ids: list[str]) -> list[Remediation]:
    if not isinstance(rule_ids, list) or any(not isinstance(x, str) or not x.strip() for x in rule_ids):
        raise ValueError("rule_ids must be a list of non-empty identifiers")
    results = []
    for rule in dict.fromkeys(rule_ids):
        family = rule if rule in RULE_GUIDANCE else ("UP" if rule.startswith("UP") else None)
        if family is None:
            guidance, risk = "Consult the exact linter rule documentation and inspect the flagged code", "No rule-specific guidance is available"
        else:
            guidance, risk = RULE_GUIDANCE[family]
        results.append(Remediation(rule, guidance, ("Add or update a focused regression test", "Run the configured linter and relevant test suite"), risk))
    return results


def to_json(items: list[Remediation]) -> str:
    return json.dumps([asdict(x) for x in items], indent=2)


if __name__ == "__main__":
    print(to_json(suggest_remediations(["F401", "B904"])))
