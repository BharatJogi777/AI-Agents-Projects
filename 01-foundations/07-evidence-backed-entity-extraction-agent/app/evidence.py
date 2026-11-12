"""Deterministic evidence verification and source-character offsets."""
from dataclasses import dataclass
from hashlib import sha256
from app.schemas import ExtractionResult

@dataclass(frozen=True, slots=True)
class EvidenceMatch:
    entity_index: int
    value: str
    entity_type: str
    evidence: str
    evidence_start: int
    evidence_end: int
    value_start: int
    value_end: int

@dataclass(frozen=True, slots=True)
class VerifiedExtraction:
    source_sha256: str
    entities: ExtractionResult
    evidence_matches: tuple[EvidenceMatch, ...]

class EvidenceVerificationError(ValueError):
    """An extracted entity cannot be anchored to the exact source text."""

class EvidenceVerifier:
    """Verify literal evidence and return stable Python-string character offsets."""
    def verify(self, source_text: str, result: ExtractionResult) -> VerifiedExtraction:
        matches = []
        for index, entity in enumerate(result.entities):
            evidence_start = source_text.find(entity.evidence)
            if evidence_start < 0:
                raise EvidenceVerificationError(f"Evidence for entity {entity.value!r} is not an exact source substring.")
            value_relative = entity.evidence.find(entity.value)
            if value_relative < 0:
                raise EvidenceVerificationError(f"Entity {entity.value!r} does not appear in its evidence quote.")
            value_start = evidence_start + value_relative
            matches.append(EvidenceMatch(index, entity.value, entity.entity_type.value, entity.evidence,
                evidence_start, evidence_start + len(entity.evidence), value_start, value_start + len(entity.value)))
        return VerifiedExtraction(sha256(source_text.encode("utf-8")).hexdigest(), result, tuple(matches))
