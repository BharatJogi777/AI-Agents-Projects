from __future__ import annotations

import re
from typing import Any

_PATTERNS = [
    re.compile(r"(?i)(authorization\\s*[:=]\\s*bearer\\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|password|secret)\\s*[:=]\\s*)[^\\s,;]+"),
    re.compile(r"\\bAKIA[0-9A-Z]{16}\\b"),
]
_SENSITIVE_KEYS = {"password", "passwd", "secret", "token", "api_key", "access_token", "authorization"}


def redact_text(value: str) -> str:
    output = value
    for pattern in _PATTERNS:
        output = pattern.sub(lambda match: (match.group(1) + "[REDACTED]") if match.lastindex else "[REDACTED]", output)
    return output


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if str(key).lower().replace("-", "_") in _SENSITIVE_KEYS
            else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact(item) for item in value)
    if isinstance(value, str):
        return redact_text(value)
    return value
