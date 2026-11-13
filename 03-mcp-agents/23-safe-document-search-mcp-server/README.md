# AG-123 — Safe document search MCP server

An in-memory search service that filters documents by principal before ranking results. It validates query identity and bounds result count.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Expose this service as a narrow MCP tool after authenticating the caller. Apply document-level ACL filtering before retrieval, not after sending results to the model. Avoid returning full source text; snippets are capped.

## Limitations
This example uses simple term frequency over in-memory records. Production search should enforce ACLs in the retrieval query, use a real index, and audit access.
