from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import httpx


class RestAdapter:
    def __init__(self, base_url: str, token: str, allowed_routes: set[str], timeout: float = 5.0):
        parsed = urlparse(base_url)
        if parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1"}:
            raise ValueError("HTTPS required for remote API")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("invalid API base URL")
        if not allowed_routes or any(not x.startswith("/") or ".." in x for x in allowed_routes):
            raise ValueError("routes must be explicit absolute paths")
        self.url, self.token, self.routes, self.timeout = base_url.rstrip("/"), token, allowed_routes, timeout

    async def get(self, route: str, params: dict[str, str] | None = None) -> dict[str, Any]:
        if route not in self.routes:
            raise PermissionError("route is not allowlisted")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.url + route, params=params,
                headers={"Authorization": f"Bearer {self.token}"} if self.token else {})
            response.raise_for_status()
            payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("API response must be a JSON object")
        return payload
