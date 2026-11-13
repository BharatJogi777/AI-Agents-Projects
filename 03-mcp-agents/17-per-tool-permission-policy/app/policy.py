"""Explicit per-tool and per-action authorization policy."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Action(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


@dataclass(frozen=True)
class Permission:
    tool: str
    action: Action
    roles: frozenset[str]
    enabled: bool = True


class Policy:
    def __init__(self, permissions: list[Permission]) -> None:
        self._rules: dict[tuple[str, Action], Permission] = {}
        for rule in permissions:
            key = (rule.tool, rule.action)
            if not rule.tool.strip() or not rule.roles:
                raise ValueError("tool and at least one role are required")
            if key in self._rules:
                raise ValueError(f"duplicate permission rule: {rule.tool}/{rule.action.value}")
            self._rules[key] = rule

    def allows(self, *, tool: str, action: Action, roles: frozenset[str]) -> bool:
        rule = self._rules.get((tool, action))
        return bool(rule and rule.enabled and roles.intersection(rule.roles))
