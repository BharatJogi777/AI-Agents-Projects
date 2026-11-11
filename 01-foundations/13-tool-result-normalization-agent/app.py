"""Convert arbitrary tool outputs into bounded, JSON-safe, redacted envelopes."""
import json
import math
from datetime import date, datetime
from typing import Any


SENSITIVE_KEYS = {"password", "token", "access_token", "refresh_token", "secret", "api_key", "authorization"}


class NormalizationError(ValueError):
    pass


def _safe(value: Any, *, depth: int, max_depth: int, max_string: int,
          max_items: int, seen: set[int], warnings: list[str]) -> Any:
    if depth > max_depth:
        warnings.append("maximum nesting depth reached")
        return "[DEPTH_LIMIT]"
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, str):
        if len(value) > max_string:
            warnings.append("string truncated")
            return value[:max_string] + "…[TRUNCATED]"
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, bytes):
        warnings.append("binary output represented as metadata")
        return {"type": "bytes", "length": len(value)}
    identity = id(value)
    if identity in seen:
        warnings.append("circular reference replaced")
        return "[CIRCULAR_REFERENCE]"
    if isinstance(value, dict):
        seen.add(identity)
        out = {}
        for index, (key, item) in enumerate(value.items()):
            if index >= max_items:
                warnings.append("mapping item limit reached")
                out["_truncated_items"] = len(value) - max_items
                break
            name = str(key)[:max_string]
            if name.lower() in SENSITIVE_KEYS:
                out[name] = "[REDACTED]"
            else:
                out[name] = _safe(item, depth=depth + 1, max_depth=max_depth,
                                  max_string=max_string, max_items=max_items,
                                  seen=seen, warnings=warnings)
        seen.remove(identity)
        return out
    if isinstance(value, (list, tuple, set)):
        seen.add(identity)
        items = list(value)
        result = [_safe(item, depth=depth + 1, max_depth=max_depth,
                        max_string=max_string, max_items=max_items,
                        seen=seen, warnings=warnings) for item in items[:max_items]]
        if len(items) > max_items:
            warnings.append("sequence item limit reached")
            result.append(f"[{len(items) - max_items} ITEMS OMITTED]")
        seen.remove(identity)
        return result
    warnings.append(f"unsupported value type: {type(value).__name__}")
    return {"type": type(value).__name__, "repr": repr(value)[:max_string]}


def normalize_tool_result(result: Any, *, ok: bool = True, max_depth: int = 6,
                          max_string: int = 4000, max_items: int = 100,
                          max_output_bytes: int = 16000) -> dict[str, Any]:
    """Return a stable envelope; never serialize unbounded or sensitive output."""
    if max_depth < 1 or max_string < 32 or max_items < 1 or max_output_bytes < 256:
        raise ValueError("normalization limits are too small")
    warnings: list[str] = []
    data = _safe(result, depth=0, max_depth=max_depth, max_string=max_string,
                 max_items=max_items, seen=set(), warnings=warnings)
    envelope = {"ok": bool(ok), "data": data, "warnings": list(dict.fromkeys(warnings))}
    encoded = json.dumps(envelope, ensure_ascii=False, separators=(",", ":"))
    if len(encoded.encode("utf-8")) > max_output_bytes:
        envelope["data"] = {"type": "omitted", "reason": "normalized output exceeded byte budget"}
        envelope["warnings"].append("output byte budget exceeded")
    return envelope
