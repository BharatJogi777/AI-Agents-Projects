# MCP server conformance tester

A small protocol-level test harness for an MCP client session. It checks initialization, tool listing shape, unique tool names, and whether each tool publishes an object input schema.

## Setup
Python 3.11+: `pip install -e ".[dev]"`; run `pytest -q`.

## Use
Import `inspect_session` and pass an initialized MCP `ClientSession`. The helper uses the public session methods `list_tools` and `ping`.

## Limits
This is a focused smoke/conformance check, not the full MCP specification test suite. It does not prove authorization, transport security, or tool correctness. Run it against a disposable test server.
