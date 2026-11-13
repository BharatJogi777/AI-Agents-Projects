"""Namespaced orchestration over independently managed MCP sessions."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol


class Session(Protocol):
    async def list_tools(self) -> Any: ...
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any: ...


class MultiServerError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ServerBinding:
    session: Session
    allowed_tools: frozenset[str]


class MultiServerClient:
    _identifier = re.compile(r"^[a-z][a-z0-9_-]{0,62}$")

    def __init__(self) -> None:
        self._servers: dict[str, ServerBinding] = {}

    def add_server(self, namespace: str, session: Session, *, allowed_tools: set[str]) -> None:
        if not isinstance(namespace, str) or not self._identifier.fullmatch(namespace):
            raise ValueError("namespace must be a lowercase identifier")
        if namespace in self._servers:
            raise MultiServerError(f"server namespace already registered: {namespace}")
        if not allowed_tools or any(
            not isinstance(name, str) or not self._identifier.fullmatch(name)
            for name in allowed_tools
        ):
            raise ValueError("allowed_tools must contain valid lowercase tool names")
        self._servers[namespace] = ServerBinding(session, frozenset(allowed_tools))

    async def discover(self) -> list[dict[str, str]]:
        discovered: list[dict[str, str]] = []
        for namespace, binding in sorted(self._servers.items()):
            response = await binding.session.list_tools()
            for tool in response.tools:
                if tool.name in binding.allowed_tools:
                    discovered.append({
                        "qualified_name": f"{namespace}.{tool.name}",
                        "server": namespace,
                        "name": tool.name,
                        "description": tool.description or "",
                    })
        return discovered

    async def call(self, qualified_name: str, arguments: dict[str, Any]) -> Any:
        if not isinstance(arguments, dict):
            raise TypeError("tool arguments must be an object")
        if not isinstance(qualified_name, str) or qualified_name.count(".") != 1:
            raise MultiServerError("tool name must use namespace.tool format")
        namespace, name = qualified_name.split(".", 1)
        binding = self._servers.get(namespace)
        if binding is None or name not in binding.allowed_tools:
            raise MultiServerError(f"tool is not available: {qualified_name}")
        return await binding.session.call_tool(name, arguments)
