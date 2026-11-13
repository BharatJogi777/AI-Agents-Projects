"""Evidence-backed CI log diagnosis without executing build commands."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Finding:
    category: str
    evidence: str
    recommendation: str

RULES = [
    ("dependency", re.compile(r"(ModuleNotFoundError|No module named|cannot find module|dependency resolution failed)", re.I), "Verify the lockfile and install step; reproduce with the pinned runtime."),
    ("test", re.compile(r"(FAILED .*::|AssertionError|tests? failed)", re.I), "Run the failing test alone and inspect the first relevant assertion or fixture."),
    ("build", re.compile(r"(compilation failed|syntax error|undefined reference|cannot compile)", re.I), "Inspect the first compiler diagnostic and confirm toolchain versions."),
    ("configuration", re.compile(r"(missing required variable|not set|configuration error|invalid config)", re.I), "Check required CI variables and configuration schema without printing secrets."),
    ("timeout", re.compile(r"(timed out|deadline exceeded|operation timeout)", re.I), "Determine whether the job is blocked, overloaded, or has an unrealistic timeout."),
    ("permission", re.compile(r"(permission denied|EACCES|access is denied)", re.I), "Check the minimum required file or runner permissions."),
]

def diagnose_ci_log(log: str, *, max_chars: int = 200_000) -> list[Finding]:
    if not isinstance(log, str):
        raise TypeError("log must be a string")
    if not 1 <= max_chars <= 1_000_000:
        raise ValueError("max_chars must be between 1 and 1000000")
    text = log[-max_chars:]
    findings = []
    for category, pattern, recommendation in RULES:
        match = pattern.search(text)
        if match:
            line = text[max(0, text.rfind("\\n", 0, match.start()) + 1):text.find("\\n", match.start()) if text.find("\\n", match.start()) >= 0 else len(text)].strip()
            findings.append(Finding(category, line[:500], recommendation))
    if not findings and text.strip():
        findings.append(Finding("unknown", "No known failure signature matched.", "Inspect the earliest error rather than the final cascade of messages."))
    return findings
