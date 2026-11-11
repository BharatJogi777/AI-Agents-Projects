# Design notes

## Model versus application responsibility

The model performs semantic identification and proposes entity types. The application owns the output contract, duplicate detection, source-boundary checks, and error handling. Never use raw model JSON as trusted application data.

## Evidence contract

An evidence quote must be a literal substring of the original input, and the extracted value must be a literal substring of that quote. This catches fabricated quotations and values detached from their citations. It does not catch a wrong entity type, incomplete extraction, or a misleading but genuine quote.

## Why fail instead of repair?

This project isolates extraction and validation. AG-008 will explore bounded schema repair and retry policies. Keeping retries out of this project makes failure behavior deterministic and testable.

## Security

The source is framed as untrusted content and the system prompt explicitly forbids following instructions inside it. Prompt wording is not a security boundary by itself: the application still validates the schema and checks evidence. Do not expose tools or side effects to this extraction-only agent.
