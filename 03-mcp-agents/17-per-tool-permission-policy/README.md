# AG-117 — Per-tool permission policy

Models permissions as exact combinations of MCP tool, action, and role. Unknown combinations deny by default.

## Features

- Distinguishes read, write, and delete actions.
- Supports multiple roles per permission.
- Supports emergency disablement of a specific rule.
- Rejects duplicate rules and empty role sets at startup.

## Run

```bash
pip install -e '.[dev]'
pytest
```

## Integration guidance

Map each MCP tool to the action it performs; do not infer permissions from tool names at runtime. Validate policy at startup, bind roles to verified principals, and add resource/tenant scope checks before execution. Treat policy changes as security-sensitive configuration.

## Limitations

This is an in-memory policy evaluator without persistence, hot reload, or resource-level ABAC. Tests are authored and require local execution.
