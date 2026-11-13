# AG-106 — MCP stdio transport client

A runnable MCP client that launches a local server as a subprocess using the official Python SDK stdio transport. It initializes the session, lists available tools, optionally invokes one named tool, and always closes the transport through async context managers.

## Requirements and setup

Python 3.11+.

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Run the sample

```bash
python -m app.client --list
python -m app.client --tool add --arguments '{"a": 12, "b": 30}'
```

The client launches `python -m app.sample_server`; no external API or model is required.

## Lifecycle

```text
StdioServerParameters
  -> stdio_client() context
  -> ClientSession() context
  -> initialize()
  -> list_tools() / call_tool()
  -> close session and subprocess transport
```

## Operational and security notes

- The subprocess command and arguments are explicit; no shell is used.
- Do not pass untrusted command strings or arbitrary server paths.
- stdio protocol messages use stdin/stdout. The sample server must write diagnostics to stderr, never stdout.
- This is a local-process transport example, not a remote network client.
