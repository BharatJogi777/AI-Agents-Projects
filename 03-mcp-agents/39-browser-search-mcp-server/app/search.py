from __future__ import annotations

from typing import Any


def validate_query(query: str, limit: int = 10) -> str:
    if not isinstance(query, str) or not query.strip() or len(query) > 500:
        raise ValueError("query must contain 1..500 characters")
    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")
    return query.strip()


def normalize_results(payload: dict[str, Any], limit: int = 10) -> list[dict[str, str]]:
    items = payload.get("results")
    if not isinstance(items, list):
        raise ValueError("search provider returned invalid results")
    output = []
    for item in items[:limit]:
        if not isinstance(item, dict):
            continue
        title, url, snippet = item.get("title"), item.get("url"), item.get("snippet", "")
        if isinstance(title, str) and isinstance(url, str):
            output.append({"title": title[:300], "url": url[:2000], "snippet": str(snippet)[:1000]})
    return output
