from __future__ import annotations

import json
import math
import re
from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from .policy import NormalizationPolicy

SENSITIVE_KEYS = frozenset({
    "password", "passwd", "pwd", "token", "accesstoken", "refreshtoken",
    "idtoken", "secret", "clientsecret", "apisecret", "apikey",
    "authorization", "proxyauthorization", "cookie", "setcookie",
    "privatekey", "credentials", "credential", "xapikey",
})
_SENSITIVE_SEPARATORS = re.compile(r"[^a-z0-9]")


class _WarningCollector:
    def __init__(self, maximum: int) -> None:
        self._maximum = maximum
        self._items: set[str] = set()
        self._overflowed = False

    def add(self, message: str) -> None:
        if message in self._items:
            return
        if len(self._items) < self._maximum:
            self._items.add(message)
        else:
            self._overflowed = True

    def values(self) -> list[str]:
        result = sorted(self._items)
        if self._overflowed:
            result.append("additional warnings omitted")
        return result


def _is_sensitive_key(key: str) -> bool:
    normalized = _SENSITIVE_SEPARATORS.sub("", key.casefold())
    return normalized in SENSITIVE_KEYS


def _safe(
    value: Any,
    depth: int,
    policy: NormalizationPolicy,
    active: set[int],
    warnings: _WarningCollector,
) -> Any:
    if depth > policy.max_depth:
        warnings.add("maximum nesting depth reached")
        return "[DEPTH_LIMIT]"

    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        # Avoid huge integer-to-decimal conversions and giant model payloads.
        if value.bit_length() > 4_096:
            warnings.add("integer too large; value omitted")
            return "[INTEGER_OMITTED]"
        return value
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        warnings.add("non-finite number replaced")
        return "[NON_FINITE_NUMBER]"
    if isinstance(value, str):
        if len(value) > policy.max_string_chars:
            warnings.add("string truncated")
            return value[:policy.max_string_chars] + "…[TRUNCATED]"
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        if not value.is_finite():
            warnings.add("non-finite decimal replaced")
            return "[NON_FINITE_NUMBER]"
        rendered = str(value)
        if len(rendered) > policy.max_string_chars:
            warnings.add("decimal string truncated")
            return rendered[:policy.max_string_chars] + "…[TRUNCATED]"
        return rendered
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, bytes):
        warnings.add("binary output represented as metadata")
        return {"type": "bytes", "length": len(value)}

    # Deliberately support only built-in dict/list/tuple containers. Avoid
    # arbitrary Mapping/Sequence protocols that can execute custom code.
    if isinstance(value, dict):
        identity = id(value)
        if identity in active:
            warnings.add("circular reference replaced")
            return "[CIRCULAR_REFERENCE]"
        active.add(identity)
        output: dict[str, Any] = {}
        try:
            for index, (key, item) in enumerate(dict.items(value)):
                if index >= policy.max_items_per_container:
                    warnings.add("mapping item limit reached")
                    output["_omitted_items"] = len(value) - index
                    break
                if not isinstance(key, str):
                    warnings.add("non-string mapping key replaced")
                    name = f"[NON_STRING_KEY_{index}]"
                else:
                    name = key[:policy.max_string_chars]
                    if len(key) > policy.max_string_chars:
                        warnings.add("mapping key truncated")
                # Redact before descending; secret values are never traversed.
                output[name] = (
                    "[REDACTED]"
                    if isinstance(key, str) and _is_sensitive_key(key)
                    else _safe(item, depth + 1, policy, active, warnings)
                )
        finally:
            active.remove(identity)
        return output

    if isinstance(value, (list, tuple)):
        identity = id(value)
        if identity in active:
            warnings.add("circular reference replaced")
            return "[CIRCULAR_REFERENCE]"
        active.add(identity)
        try:
            output = [
                _safe(item, depth + 1, policy, active, warnings)
                for item in value[:policy.max_items_per_container]
            ]
        finally:
            active.remove(identity)
        omitted = len(value) - len(output)
        if omitted:
            warnings.add("sequence item limit reached")
            output.append(f"[{omitted} ITEMS OMITTED]")
        return output

    warnings.add(f"unsupported value type: {type(value).__name__}")
    return {"type": type(value).__name__, "value": "[UNSUPPORTED]"}


def normalize_tool_result(
    result: Any,
    *,
    ok: bool = True,
    max_depth: int = 6,
    max_string: int = 4_000,
    max_items: int = 100,
    max_output_bytes: int = 16_000,
    policy: NormalizationPolicy | None = None,
) -> dict[str, Any]:
    """Return a bounded, JSON-compatible tool result envelope.

    The function does not invoke repr() or custom serialization methods on
    arbitrary objects. Sensitive dictionary values are replaced before
    recursive traversal. If the full envelope exceeds its byte budget, the
    data is omitted and a compact fallback envelope is returned.
    """
    if not isinstance(ok, bool):
        raise TypeError("ok must be a boolean")
    if policy is not None and (
        max_depth != 6 or max_string != 4_000 or max_items != 100 or max_output_bytes != 16_000
    ):
        raise ValueError("pass either policy or individual limits, not both")

    active_policy = policy or NormalizationPolicy(
        max_depth=max_depth,
        max_string_chars=max_string,
        max_items_per_container=max_items,
        max_output_bytes=max_output_bytes,
    )
    warnings = _WarningCollector(active_policy.max_warnings)
    data = _safe(result, 0, active_policy, set(), warnings)
    envelope = {"ok": ok, "data": data, "warnings": warnings.values()}

    encoded = json.dumps(
        envelope,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    if len(encoded) <= active_policy.max_output_bytes:
        return envelope

    fallback = {
        "ok": ok,
        "data": {"type": "omitted", "reason": "normalized output exceeded byte budget"},
        "warnings": ["output byte budget exceeded"],
    }
    # Policy requires >=256 bytes; this compact envelope is safely below it.
    return fallback
