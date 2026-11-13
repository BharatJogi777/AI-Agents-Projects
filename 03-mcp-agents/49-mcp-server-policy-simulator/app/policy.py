from dataclasses import dataclass


@dataclass(frozen=True)
class AccessRequest:
    principal: str
    tool: str
    scopes: frozenset[str] = frozenset()


@dataclass(frozen=True)
class PolicyRule:
    principals: frozenset[str]
    tools: frozenset[str]
    required_scopes: frozenset[str] = frozenset()
    effect: str = "allow"

    def __post_init__(self) -> None:
        if self.effect not in {"allow", "deny"}:
            raise ValueError("effect must be allow or deny")
        if not self.principals or not self.tools:
            raise ValueError("rules must name principals and tools")


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str


class PolicyEngine:
    def __init__(self, rules: list[PolicyRule]):
        self._rules = tuple(rules)

    def evaluate(self, request: AccessRequest) -> Decision:
        if not request.principal.strip() or not request.tool.strip():
            return Decision(False, "invalid_identity_or_tool")
        matching = [
            rule for rule in self._rules
            if request.principal in rule.principals and request.tool in rule.tools
        ]
        if any(rule.effect == "deny" for rule in matching):
            return Decision(False, "explicit_deny")
        grants = [r for r in matching if r.effect == "allow"]
        if not grants:
            return Decision(False, "no_matching_grant")
        if not any(rule.required_scopes.issubset(request.scopes) for rule in grants):
            return Decision(False, "missing_required_scope")
        return Decision(True, "matched_allow_rule")
