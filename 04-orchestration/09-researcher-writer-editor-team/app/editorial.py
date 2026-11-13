from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Finding:
    claim: str
    source: str

@dataclass(frozen=True)
class Draft:
    text: str
    cited_sources: tuple[str, ...]

@dataclass(frozen=True)
class EditorialResult:
    draft: Draft
    edited_text: str

class EditorialTeam:
    def __init__(self, researcher: Callable[[str], list[Finding]], writer: Callable[[str, list[Finding]], Draft], editor: Callable[[Draft], str]):
        self.researcher, self.writer, self.editor = researcher, writer, editor

    def run(self, topic: str) -> EditorialResult:
        if not topic or not topic.strip(): raise ValueError("topic is required")
        findings = self.researcher(topic)
        if not isinstance(findings, list) or any(not isinstance(x, Finding) or not x.claim.strip() or not x.source.strip() for x in findings):
            raise ValueError("researcher must return findings with claims and source identifiers")
        draft = self.writer(topic, findings)
        if not isinstance(draft, Draft) or not draft.text.strip():
            raise ValueError("writer must return a non-empty Draft")
        known = {f.source for f in findings}
        if not set(draft.cited_sources).issubset(known):
            raise ValueError("draft cites a source not present in research findings")
        edited = self.editor(draft)
        if not isinstance(edited, str) or not edited.strip(): raise ValueError("editor returned empty text")
        return EditorialResult(draft, edited)
