from __future__ import annotations

from typing import Any


def validate_promql(query: str) -> str:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("PromQL query is required")
    if len(query) > 2000:
        raise ValueError("PromQL query exceeds 2000 characters")
    if any(ord(ch) < 32 and ch not in "\\t\\n" for ch in query):
        raise ValueError("query contains control characters")
    return query.strip()


def normalize_result(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if payload.get("status") != "success":
        raise RuntimeError("Prometheus query failed")
    data = payload.get("data") or {}
    result = data.get("result")
    if not isinstance(result, list):
        raise ValueError("invalid Prometheus result shape")
    return [
        {"metric": item.get("metric", {}), "value": item.get("value") or item.get("values")}
        for item in result[:500]
        if isinstance(item, dict)
    ]
