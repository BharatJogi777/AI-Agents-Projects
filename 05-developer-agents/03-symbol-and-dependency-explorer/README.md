# Symbol and Dependency Explorer

AG-203 is a repository-aware developer utility. It favors static inspection and bounded inputs; it does not execute repository code or apply changes.

## Features

- Framework-neutral Python implementation
- Input validation and explicit error handling
- Tests for successful and failure paths

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Safety and limitations

Treat repository contents as untrusted. Run with least-privilege filesystem access, enforce file/size limits, and review outputs before acting on them. This reference utility is local and in-process; it does not connect to Git hosting APIs.
