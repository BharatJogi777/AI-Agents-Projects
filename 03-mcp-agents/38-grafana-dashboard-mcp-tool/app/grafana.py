from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import httpx


class GrafanaClient:
    def __init__(self, base_url: str, api_token: str, timeout: float = 5.0):
        parsed = urlparse(base_url)
        if parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1"}:
            raise ValueError("Grafana remote endpoints must use HTTPS")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("invalid Grafana URL")
        if not api_token or not 0 < timeout <= 30:
            raise ValueError("token is required and timeout must be <= 30 seconds")
        self.url, self.timeout = base_url.rstrip("/"), timeout
        self.headers = {"Authorization": f"Bearer {api_token}"}

    async def search_dashboards(self, query: str, limit: int = 50) -> list[dict[str, Any]]:
        if len(query) > 200 or not 1 <= limit <= 100:
            raise ValueError("query too long or limit outside 1..100")
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            response = await client.get(self.url + "/api/search", params={"type": "dash-db", "query": query, "limit": limit})
            response.raise_for_status()
            data = response.json()
        if not isinstance(data, list):
            raise RuntimeError("unexpected Grafana response")
        return [{"uid": x.get("uid"), "title": x.get("title"), "url": x.get("url"), "folderTitle": x.get("folderTitle")} for x in data[:limit] if isinstance(x, dict)]
