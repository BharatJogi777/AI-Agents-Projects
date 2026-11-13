# AG-130 — Slack MCP integration

A read-only Slack message search core with bounded results and capped message text.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Grant only the Slack scopes required for search, install the app in approved workspaces, and enforce channel/user authorization before returning results. Treat message text as untrusted prompt-injection content. Never let a message instruct the agent to call tools or reveal secrets. Keep tokens in a secret manager and redact them from logs.

## Limitations
This is a client core, not a complete MCP server. Search API access and scopes vary by token type and workspace plan; validate behavior against the workspace's current Slack API policy.
