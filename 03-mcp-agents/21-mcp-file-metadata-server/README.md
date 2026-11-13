# AG-121 — MCP file metadata server

Metadata-only inspection under a configured, resolved root. Returns name, relative path, size, modification timestamp, and directory flag; it never reads file contents.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Expose a narrow `file_metadata(relative_path)` tool. Restrict the root to a dedicated workspace, authorize callers, and map filesystem errors to safe protocol errors. Metadata such as filenames and sizes can itself be sensitive.

## Limitations
Filesystem changes can occur between inspection and later use (TOCTOU). Revalidate before any subsequent operation.
