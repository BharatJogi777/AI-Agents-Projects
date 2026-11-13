# MCP tool contract test harness

Validate tool descriptors, input schemas, and returned value types independently of a live MCP server.

## Setup
Python 3.11+: `pip install -e ".[dev]"`; run `pytest -q`.

## Run
Start with `python -m app.server`. Use `inspect_tool_contract` to check a descriptor and `inspect_arguments` to validate a JSON argument object.

## Security
Schema validation is not authorization. Apply permission checks before invocation, bound payload sizes, and never trust a tool description as executable instructions.
