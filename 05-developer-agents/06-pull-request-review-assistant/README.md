# Pull Request Review Assistant

A deterministic review pipeline that inspects a unified diff and produces actionable, evidence-linked findings. It deliberately does not modify files, approve, or merge pull requests.

## Features
- Parses unified diffs into file and hunk records.
- Flags risky patterns (debug statements, broad exception handlers, hard-coded credentials, disabled TLS checks, and suspicious destructive commands).
- Attaches each finding to a changed line when possible.
- Supports severity filtering and stable JSON output.
- Treats the diff as untrusted input; findings are suggestions, not proof.

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m app.review sample.diff
pytest
```

## Safety and limitations
This is a static heuristic assistant, not a substitute for tests, human review, SAST, or secret scanning. It never executes diff content and never applies changes. Reviewers must verify context and false positives before acting.
