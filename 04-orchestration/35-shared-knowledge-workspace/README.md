# AG-185: Shared knowledge workspace

## Purpose
A shared knowledge workspace for agents that supports source attribution, confidence metadata, controlled updates, and retrieval by topic.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
Knowledge entries are keyed by stable IDs and retain source agent, topic, confidence, and update revision. Search is a deterministic in-memory topic filter; production systems should replace it with an indexed durable store and enforce access policies.

## Production considerations
Validate provenance and content, define retention and deletion policies, protect sensitive data, and treat retrieved content as untrusted. Add durable persistence, audit logs, access control, and observability before deployment.

Tests are authored but not executed in the target environment.