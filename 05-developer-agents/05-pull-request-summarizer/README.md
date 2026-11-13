# Pull Request Summarizer

AG-205 summarizes a unified diff into changed-file, addition, deletion, and binary-file statistics.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Safety and limitations

This tool parses diff text only; it does not fetch pull requests, inspect remote repositories, or approve changes. Treat diff content as untrusted and keep upstream diff-size limits in place.
