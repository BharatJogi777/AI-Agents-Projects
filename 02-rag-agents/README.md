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

## Retrieval projects (AG-061–AG-070)

- [Document deduplication agent](./11-document-deduplication-agent/) — Detect exact duplicates using SHA-256 and normalized text; report groups without automatically deleting source records.
- [Document metadata extractor](./12-document-metadata-extractor/) — Extract deterministic file metadata including name, media type, byte size, modification time, and content digest.
- [Semantic chunking pipeline](./13-semantic-chunking-pipeline/) — Split text at injected semantic similarity boundaries while retaining source offsets.
- [Parent-child chunk retrieval](./14-parent-child-chunk-retrieval/) — Store larger parent passages and smaller searchable child chunks, then expand matched children to parent context.
- [Sliding-window chunker](./15-sliding-window-chunker/) — Generate overlapping text windows with stable offsets and validated size and overlap.
- [Hybrid keyword-vector search agent](./16-hybrid-keyword-vector-search-agent/) — Combine lexical and vector rankings using reciprocal rank fusion.
- [Metadata-filtered retrieval agent](./17-metadata-filtered-retrieval-agent/) — Apply validated allowlisted metadata filters without evaluating user-supplied expressions.
- [Query rewriting agent](./18-query-rewriting-agent/) — Expand ambiguous queries using an injected rewriter while retaining the original and bounding variants.
- [Multi-query retrieval agent](./19-multi-query-retrieval-agent/) — Retrieve across query variants, deduplicate candidates, and fuse ranks using reciprocal rank fusion.
- [HyDE retrieval agent](./20-hyde-retrieval-agent/) — Generate a hypothetical document for query expansion while never treating generated text as evidence.

All ten include deterministic application code, standalone tests, README instructions, and dependency metadata. Tests are authored but not locally executed.
