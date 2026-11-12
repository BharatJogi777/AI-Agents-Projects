# Design notes

## Model versus application responsibility

The model performs semantic identification and proposes entity types. The application owns the output contract, duplicate detection, source-boundary checks, and error handling. Never use raw model JSON as trusted application data.

## Evidence contract and offsets

Every evidence quote must be a literal substring of the original input, and the extracted value must be a literal substring of that quote. The verifier returns Python-string character offsets for both the quote and entity value, plus a SHA-256 fingerprint of the exact UTF-8 source. Downstream systems can highlight evidence and bind an extraction to a source version.

Offsets are zero-based Python Unicode code-point positions, not UTF-8 byte offsets or browser UTF-16 offsets. Convert explicitly for other indexing conventions. If evidence appears more than once, the first exact occurrence is selected. This is deterministic but may not be the semantically intended occurrence.

These checks catch fabricated quotations and values detached from citations. They do not catch a wrong entity type, incomplete extraction, or a misleading but genuine quote.

## Prompt framing

The source is JSON-string encoded before being placed in the user message. This prevents source text from syntactically closing a hand-written XML-like delimiter. It does not make prompt injection impossible. Treat model output as untrusted and never give this extraction-only component tools or side effects.

## Why fail instead of repair?

This project isolates extraction and validation. AG-008 explores bounded schema repair and retry policies. Keeping retries out of this project makes failure behavior deterministic and testable.

## Security and operations

Input and output byte limits bound memory and provider payload sizes. Provider errors are sanitized by the adapter. Do not log source text or full model output by default: documents may contain personal, confidential, or regulated data. A source hash is a fingerprint, not encryption or anonymization.
