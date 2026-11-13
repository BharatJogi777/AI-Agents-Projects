# MCP secret redaction middleware

Redacts common credential patterns and sensitive dictionary keys before diagnostic output or audit logging.

## Setup
Python 3.11+: `pip install -e ".[dev]"`; run `pytest -q`.

## Run
`python -m app.server` starts an MCP demonstration tool.

## Security
Pattern-based redaction is not a complete DLP system. Add organization-specific patterns, avoid logging request bodies by default, restrict log access, and rotate any credential that may already have been exposed.
