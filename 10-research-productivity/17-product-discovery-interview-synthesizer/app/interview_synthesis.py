"""Synthesize interview notes while retaining evidence provenance."""
from collections import defaultdict
from dataclasses import dataclass

@dataclass(frozen=True)
class Theme:
    name: str
    evidence: tuple[str, ...]
    interview_ids: tuple[str, ...]

def synthesize_interviews(*, interviews: list[dict]) -> list[Theme]:
    if not isinstance(interviews, list):
        raise TypeError("interviews must be a list")
    grouped = defaultdict(lambda: {"evidence": [], "ids": []})
    for index, interview in enumerate(interviews, 1):
        if not isinstance(interview, dict):
            raise TypeError(f"interview {index} must be a dictionary")
        iid = interview.get("id")
        if not isinstance(iid, str) or not iid.strip():
            raise ValueError(f"interview {index} requires an id")
        observations = interview.get("observations")
        if not isinstance(observations, list):
            raise ValueError(f"interview {iid} observations must be a list")
        for observation in observations:
            if not isinstance(observation, dict):
                raise TypeError("each observation must be a dictionary")
            theme, quote = observation.get("theme"), observation.get("evidence")
            if not isinstance(theme, str) or not theme.strip() or not isinstance(quote, str) or not quote.strip():
                raise ValueError("each observation requires a theme and evidence")
            key = theme.strip()
            grouped[key]["evidence"].append(quote.strip())
            grouped[key]["ids"].append(iid.strip())
    return [Theme(name, tuple(data["evidence"]), tuple(dict.fromkeys(data["ids"])))
            for name, data in sorted(grouped.items())]
