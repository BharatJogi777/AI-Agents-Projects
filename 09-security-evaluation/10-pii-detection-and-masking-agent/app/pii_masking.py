"""Detect and mask common PII patterns with source offsets."""
import re

def detect_and_mask_pii(*, text: str) -> dict[str, object]:
    if not isinstance(text, str): raise TypeError("text must be a string")
    patterns = {"email": r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "phone": r"\b(?:\+?\d[\d .()-]{7,}\d)\b", "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"}
    spans = []
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            if kind == "ipv4" and any(int(part) > 255 for part in match.group().split(".")): continue
            spans.append((match.start(), match.end(), kind))
    spans.sort()
    selected = []
    for item in spans:
        if selected and item[0] < selected[-1][1]: continue
        selected.append(item)
    masked = text
    for start, end, kind in reversed(selected): masked = masked[:start] + f"[{kind.upper()}]" + masked[end:]
    return {"masked_text": masked, "findings": [{"type":kind,"start":start,"end":end} for start,end,kind in selected], "count":len(selected)}
