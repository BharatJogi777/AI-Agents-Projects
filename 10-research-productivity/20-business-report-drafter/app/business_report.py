"""Create a traceable business report from caller-provided facts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class BusinessReport:
    title: str
    executive_summary: str
    key_findings: tuple[str, ...]
    caveats: tuple[str, ...]
    source_labels: tuple[str, ...]

def draft_report(*, title: str, metrics: list[dict], observations: list[str], caveats: list[str] | None = None) -> BusinessReport:
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a non-empty string")
    if not isinstance(metrics, list) or not isinstance(observations, list):
        raise TypeError("metrics and observations must be lists")
    caveats = [] if caveats is None else caveats
    if not isinstance(caveats, list):
        raise TypeError("caveats must be a list")
    findings=[]
    sources=[]
    for metric in metrics:
        if not isinstance(metric, dict):
            raise TypeError("each metric must be a dictionary")
        name, value, source = metric.get("name"), metric.get("value"), metric.get("source")
        if not isinstance(name, str) or not name.strip() or value is None:
            raise ValueError("each metric requires a name and value")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"metric {name} requires a source")
        findings.append(f"{name.strip()}: {value} (source: {source.strip()})")
        sources.append(source.strip())
    for observation in observations:
        if not isinstance(observation, str) or not observation.strip():
            raise ValueError("observations must be non-empty strings")
        findings.append(observation.strip())
    if any(not isinstance(c, str) or not c.strip() for c in caveats):
        raise ValueError("caveats must be non-empty strings")
    summary = f"{len(metrics)} metrics and {len(observations)} observations supplied for review."
    if not findings:
        summary = "No findings were supplied; add evidence before drawing conclusions."
    return BusinessReport(title.strip(), summary, tuple(findings), tuple(c.strip() for c in caveats), tuple(dict.fromkeys(sources)))
