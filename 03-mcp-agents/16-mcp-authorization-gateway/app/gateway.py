"""Fail-closed authorization gateway independent of transport/auth provider."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[str]
    active: bool = True


@dataclass(frozen=True)
class ToolGrant:
    tool: str
    allowed_roles: frozenset[str]


class AuthorizationDenied(PermissionError):
    pass


class AuthorizationGateway:
    def __init__(
        self,
        grants: Mapping[str, ToolGrant],
        *,
        audit: Callable[[dict[str, str]], None] | None = None,
    ) -> None:
        self._grants = dict(grants)
        self._audit = audit or (lambda _event: None)

    def authorize(self, principal: Principal, tool_name: str) -> None:
        grant = self._grants.get(tool_name)
        allowed = (
            principal.active
            and bool(principal.subject.strip())
            and grant is not None
            and bool(principal.roles & grant.allowed_roles)
        )
        self._audit({
            "subject": principal.subject or "anonymous",
            "tool": tool_name,
            "decision": "allow" if allowed else "deny",
        })
        if not allowed:
            raise AuthorizationDenied(f"principal is not authorized for tool: {tool_name}")
