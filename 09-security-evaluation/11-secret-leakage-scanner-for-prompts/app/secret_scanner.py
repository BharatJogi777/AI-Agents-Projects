"""Scan prompt text for likely credentials and secret material."""
import re

def scan_prompt(*, prompt: str) -> dict[str, object]:
    if not isinstance(prompt, str): raise TypeError("prompt must be a string")
    patterns = {"private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "api_token": r"(?i)\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{20,})\b", "assigned_secret": r"(?i)\b(?:password|api[_-]?key|secret|access[_-]?token)\s*[:=]\s*[^\s,;]{4,}"}
    findings = []
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, prompt): findings.append({"type":kind,"start":match.start(),"end":match.end(),"preview":"[REDACTED]"})
    findings.sort(key=lambda x:x["start"])
    return {"contains_possible_secret":bool(findings),"findings":findings,"count":len(findings)}
