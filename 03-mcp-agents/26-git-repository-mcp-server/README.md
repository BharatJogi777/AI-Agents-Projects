# AG-126 — Git repository MCP server

A read-only Git inspection adapter exposing current branch, latest commit metadata, and short working-tree status.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Subprocess arguments are passed as an array (never through a shell), execution has a timeout, and errors do not echo arbitrary command output. Mount only repositories the agent is authorized to inspect.

## Security
Do not add arbitrary Git command execution, hooks, checkout, reset, or push to an agent-facing tool. Git repositories may contain malicious configuration; run in a restricted environment.

## Limitations
This is a local subprocess adapter and assumes the Git executable is installed.
