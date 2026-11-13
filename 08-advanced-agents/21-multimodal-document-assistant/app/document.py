"""Assemble validated multimodal document parts without inventing extracted content."""
from dataclasses import dataclass

SUPPORTED = {"text", "image", "audio", "table", "pdf"}
@dataclass(frozen=True)
class Part:
    part_id: str
    media_type: str
    source: str
    extracted_text: str = ""
    confidence: float = 1.0

@dataclass(frozen=True)
class DocumentPackage:
    parts: tuple[Part, ...]
    text: str
    needs_review: tuple[str, ...]

def assemble_document(parts: list[Part]) -> DocumentPackage:
    if not parts:
        raise ValueError("at least one part is required")
    seen, review, fragments = set(), [], []
    accepted = []
    for part in parts:
        if not part.part_id.strip() or part.part_id in seen:
            raise ValueError("part IDs must be non-empty and unique")
        seen.add(part.part_id)
        if part.media_type not in SUPPORTED:
            raise ValueError(f"unsupported media type: {part.media_type}")
        if not part.source.strip():
            raise ValueError("source is required for provenance")
        if not 0 <= part.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if part.confidence < 0.8:
            review.append(part.part_id)
        accepted.append(part)
        if part.extracted_text.strip():
            fragments.append(f"[{part.part_id}:{part.media_type}] {part.extracted_text.strip()}")
    return DocumentPackage(tuple(accepted), "\n".join(fragments), tuple(review))
