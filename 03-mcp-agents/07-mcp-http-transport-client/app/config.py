"""Validated environment configuration for the remote MCP client."""
from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class ClientConfig:
    server_url: str
    bearer_token: str | None = None

    @classmethod
    def from_env(cls) -> "ClientConfig":
        url = os.getenv("MCP_SERVER_URL", "").strip()
        token = os.getenv("MCP_BEARER_TOKEN") or None
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("MCP_SERVER_URL must be an absolute HTTP(S) URL")
        local_hosts = {"localhost", "127.0.0.1", "::1"}
        if parsed.scheme != "https" and parsed.hostname not in local_hosts:
            raise ValueError("HTTPS is required for non-local MCP endpoints")
        if parsed.username or parsed.password:
            raise ValueError("credentials must not be embedded in MCP_SERVER_URL")
        return cls(server_url=url, bearer_token=token)
