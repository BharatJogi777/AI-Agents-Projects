# MCP prompt-injection boundary demo

Demonstrates the trust boundary between trusted application instructions and untrusted MCP tool output. Tool results are wrapped as data with an explicit provenance marker; they are never concatenated into the trusted instruction string.

## Setup
Python 3.11+: `pip install -e ".[dev]"`; run `pytest -q`.

## Run
`python -m app.server` starts a small MCP server exposing a demonstration wrapper.

## Security note
Delimiters and provenance labels are defense-in-depth, not a prompt-injection solution. The model may still be influenced by malicious content. Enforce authorization and side-effect policies in deterministic application code, and require explicit approval for consequential actions.
