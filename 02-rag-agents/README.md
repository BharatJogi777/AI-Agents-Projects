# RAG and Data Agents

Build a grounded knowledge or data workflow. Answers must expose evidence, respect access filters, and abstain when retrieval is insufficient.

## Catalogue scope

This track contains 50 project specifications in the root [project catalogue](../docs/PROJECT_CATALOG.md) and machine-readable [JSON catalogue](../catalogue/projects.json). Catalogue entries are not claims of completed implementations.

## Implementation expectations

- Give every project a standalone purpose, explicit inputs and outputs, and a reproducible local run path.
- Keep model calls behind a small adapter; keep validation, permissions, and side effects in deterministic code.
- Add unit tests for normal behavior and important failure paths.
- Document model requirements, resource usage, limitations, and safety boundaries.
- Use the maturity labels in [PROJECT_STANDARD.md](../docs/PROJECT_STANDARD.md).

## Project status

Projects are implemented in priority order. Check the catalogue for current status; do not infer status from a folder existing.

## Implemented projects (AG-051–AG-060)

These first ten projects provide format-specific extraction and incremental ingestion building blocks:

- [PDF question-answering agent](./01-pdf-question-answering-agent/) — Extract page-aware text from PDF files and return bounded evidence snippets with page numbers for downstream grounded answers.
- [DOCX knowledge assistant](./02-docx-knowledge-assistant/) — Extract DOCX paragraphs and table rows in document order, retaining structural labels so retrieved evidence can be traced to its source.
- [Markdown documentation assistant](./03-markdown-documentation-assistant/) — Split Markdown documentation into heading-aware chunks while retaining heading paths, source line ranges, and original text for citations.
- [HTML knowledge-base agent](./04-html-knowledge-base-agent/) — Extract readable HTML text while excluding script, style, and hidden content; retain headings and links as text for safer knowledge ingestion.
- [CSV question-answering agent](./05-csv-question-answering-agent/) — Turn CSV rows into evidence-bearing records with row numbers, strict headers, bounded file size, and safe handling of quoted delimiters.
- [Excel workbook analyst](./06-excel-workbook-analyst/) — Read Excel worksheets in read-only mode, preserve sheet and row provenance, and bound workbook size and row counts.
- [JSON dataset assistant](./07-json-dataset-assistant/) — Normalize JSON objects and arrays into bounded records with stable JSON paths and canonical serialization for evidence and indexing.
- [Multi-format document ingester](./08-multi-format-document-ingester/) — Provide one bounded ingestion interface for TXT, Markdown, HTML, CSV, JSON, PDF, DOCX, and XLSX while retaining source-specific provenance.
- [Directory watcher ingestion agent](./09-directory-watcher-ingestion-agent/) — Poll a document directory safely and emit deterministic created, modified, and deleted events using content hashes without following symlinks.
- [Incremental document indexer](./10-incremental-document-indexer/) — Maintain a transactional SQLite document and chunk index using content hashes, deterministic chunk IDs, and unchanged-document skips.

All ten have standalone tests and dependency metadata. Tests are authored but require local execution. These are ingestion components, not complete LLM-backed RAG assistants.
