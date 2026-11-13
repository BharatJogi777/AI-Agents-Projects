# AG-122 — Read-only filesystem MCP server

A confined read-only workspace service for MCP resources or tools.

## Security controls
- Paths resolve beneath one configured root, including symlink targets.
- Directory listing includes only files contained in the workspace.
- UTF-8 reads are bounded by a configurable maximum size.
- No write, delete, rename, or permission-changing operation exists.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Run with a dedicated low-privilege OS account and mount only the intended workspace. Apply per-user authorization and audit reads. Consider race-resistant descriptor-based opening and OS sandboxing for untrusted workloads.

## Limitations
This is not a complete OS sandbox and does not eliminate every filesystem race. Never mount secrets or host system directories.
