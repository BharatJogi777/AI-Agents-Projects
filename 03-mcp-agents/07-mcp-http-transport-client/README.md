# AG-107 — MCP HTTP transport client

Connect to a remote MCP server using the official Python SDK Streamable HTTP transport. The client initializes a session, lists tools, and optionally invokes one tool.

## Setup

Python 3.11+.

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Run

Start an MCP server that exposes Streamable HTTP, then:

```bash
export MCP_SERVER_URL=http://127.0.0.1:8000/mcp
python -m app.client --list
python -m app.client --tool search --arguments '{"query":"incident response"}'
```

Optional bearer authentication can be supplied with `MCP_BEARER_TOKEN`. Do not put tokens in command history or commit them.

## Design and safety

- Uses Streamable HTTP, not the legacy SSE transport.
- Requires an explicit HTTP(S) endpoint; HTTPS is required outside localhost unless explicitly overridden for development.
- Sends bearer credentials only through the Authorization header.
- Uses SDK context managers to close the session and HTTP streams.
- Treats server tool metadata and results as untrusted.
- This client does not implement retries; retry policy for side-effecting calls must be designed per tool.
