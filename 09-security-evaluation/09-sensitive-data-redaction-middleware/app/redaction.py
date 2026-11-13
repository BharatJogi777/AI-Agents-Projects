"""Redact common sensitive patterns from text before logging or forwarding."""
import re

def redact_sensitive_text(*, text: str, extra_patterns: list[str] | None = None) -> dict[str, object]:
    if not isinstance(text, str): raise TypeError("text must be a string")
    patterns = [(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[REDACTED_EMAIL]"), (r"\b(?:\+?\d[\d .()-]{7,}\d)\b", "[REDACTED_PHONE]"), (r"(?i)\b(?:api[_-]?key|token|password)\s*[:=]\s*[^\s,;]+", "[REDACTED_SECRET]")]
    for pattern in extra_patterns or []:
        if not isinstance(pattern, str) or len(pattern) > 300: raise ValueError("extra patterns must be strings up to 300 characters")
        patterns.append((pattern, "[REDACTED_CUSTOM]"))
    result, counts = text, {}
    for pattern, replacement in patterns:
        result, count = re.subn(pattern, replacement, result)
        counts[replacement] = counts.get(replacement, 0) + count
    return {"text": result, "redaction_counts": counts}
