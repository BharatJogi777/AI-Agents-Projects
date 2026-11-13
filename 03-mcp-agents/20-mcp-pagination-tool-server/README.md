# AG-120 — MCP pagination tool server

A reusable bounded pagination function for MCP tools returning collections. Results contain items, offset, limit, total count, and a `has_more` flag. Invalid offsets and limits are rejected.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Expose validated offset/limit arguments and serialize the page metadata. For large or changing datasets, prefer cursor/keyset pagination with a stable sort key; never expose raw database cursors or trust client-provided SQL fragments.

## Limitations
This example paginates an in-memory sequence. Production repositories should push pagination into the database and enforce deterministic ordering.
