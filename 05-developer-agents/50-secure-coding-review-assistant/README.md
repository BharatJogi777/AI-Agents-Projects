# Secure coding review assistant

Conservative Python AST checks for risky constructs. Findings include line numbers and require human review.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Safety and limitations

Static heuristics are incomplete and can produce false positives or miss vulnerabilities. This tool does not execute analyzed code, modify files, or replace a dedicated SAST tool and security review.
