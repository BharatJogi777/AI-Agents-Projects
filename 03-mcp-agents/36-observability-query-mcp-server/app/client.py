from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import httpx


class ObservabilityClient:
    def __init__(self, base_url: str, token: str | None = None, timeout: float = 5.0):
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1"}:
            raise ValueError("HTTPS is required except for localhost")
        if not 0 < timeout <= 30:
            raise ValueError("timeout must be between 0 and 30 seconds")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    async def query(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        if path not in {"/api/v1/query", "/api/v1/query_range"}:
            raise ValueError("unsupported observability API path")
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            response = await client.get(self.base_url + path, params=params)
            response.raise_for_status()
            payload = response.json()
        if not isinstance(payload, dict) or payload.get("status") != "success":
            raise RuntimeError("observability backend returned an unsuccessful response")
        return payload
