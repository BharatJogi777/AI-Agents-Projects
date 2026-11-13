"""Collision-safe routing names for tools from multiple MCP servers."""
from __future__ import annotations

import re


_NAME = re.compile(r"^[a-z][a-z0-9_-]{0,62}$")


class NamespaceError(ValueError):
    pass


class NamespaceRegistry:
    def __init__(self) -> None:
        self._servers: dict[str, frozenset[str]] = {}

    def register(self, namespace: str, tools: list[str]) -> None:
        if not isinstance(namespace, str) or not _NAME.fullmatch(namespace):
            raise NamespaceError("namespace must be a lowercase identifier")
        if namespace in self._servers:
            raise NamespaceError(f"namespace already registered: {namespace}")
        if not tools:
            raise NamespaceError("server must expose at least one tool")
        if any(not isinstance(name, str) or not _NAME.fullmatch(name) for name in tools):
            raise NamespaceError("tool names must be lowercase identifiers")
        if len(tools) != len(set(tools)):
            raise NamespaceError("duplicate tool names within server")
        self._servers[namespace] = frozenset(tools)

    def resolve(self, qualified_name: str) -> tuple[str, str]:
        if not isinstance(qualified_name, str) or qualified_name.count(".") != 1:
            raise NamespaceError("tool name must use namespace.tool format")
        namespace, tool = qualified_name.split(".", 1)
        if namespace not in self._servers or tool not in self._servers[namespace]:
            raise NamespaceError(f"unknown qualified tool: {qualified_name}")
        return namespace, tool

    def list_tools(self) -> list[str]:
        return sorted(f"{namespace}.{tool}" for namespace, tools in self._servers.items() for tool in tools)
