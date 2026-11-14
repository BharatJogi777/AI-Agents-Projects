"""Organize supplied study metadata into a traceable literature-review outline."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewOutline:
    themes: tuple[tuple[str, tuple[str, ...]], ...]
    limitations: tuple[str, ...]
    duplicate_study_ids: tuple[str, ...]
    included_study_ids: tuple[str, ...]

def build_review_outline(*, studies: list[dict]) -> ReviewOutline:
    if not isinstance(studies, list):
        raise ValueError("studies must be a list")
    themes: dict[str, list[str]] = {}
    limitations: list[str] = []
    seen: set[str] = set()
    duplicates: list[str] = []
    included: list[str] = []
    for study in studies:
        if not isinstance(study, dict):
            raise ValueError("each study must be a dictionary")
        required = ("study_id", "title", "theme", "limitations")
        if any(not isinstance(study.get(k), str) or not study[k].strip() for k in required):
            raise ValueError("each study requires non-empty study_id, title, theme, and limitations")
        key = (study.get("doi") or study["study_id"]).strip().lower()
        if key in seen:
            duplicates.append(study["study_id"])
            continue
        seen.add(key)
        included.append(study["study_id"])
        themes.setdefault(study["theme"].strip(), []).append(study["study_id"])
        limitations.append(f"{study['study_id']}: {study['limitations'].strip()}")
    grouped = tuple((name, tuple(ids)) for name, ids in sorted(themes.items()))
    return ReviewOutline(grouped, tuple(limitations), tuple(duplicates), tuple(included))
