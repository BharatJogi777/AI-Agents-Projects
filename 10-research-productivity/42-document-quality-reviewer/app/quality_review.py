"""Run transparent structural checks over supplied document text."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    message: str
    line: int | None = None

def review_document(text: str, required_sections: tuple[str, ...] = (), max_line_length: int = 120) -> list[Finding]:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("document text is required")
    if max_line_length <= 0:
        raise ValueError("max_line_length must be positive")
    lines = text.splitlines()
    findings = []
    headings = {line.lstrip("# ").strip().casefold() for line in lines if line.startswith("#")}
    for section in required_sections:
        if not section.strip():
            raise ValueError("required section names cannot be empty")
        if section.casefold() not in headings:
            findings.append(Finding("required_section", "warning", f"Missing section: {section}"))
    for number, line in enumerate(lines, 1):
        if len(line) > max_line_length:
            findings.append(Finding("line_length", "info", f"Line exceeds {max_line_length} characters", number))
        if line.rstrip() != line:
            findings.append(Finding("trailing_whitespace", "info", "Line has trailing whitespace", number))
    if not text.endswith("\n"):
        findings.append(Finding("final_newline", "info", "Document does not end with a newline"))
    return findings
