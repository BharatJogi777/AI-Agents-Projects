# Kubernetes deployment reviewer

## Purpose

Review Kubernetes Deployment specifications for rollout safety, availability, resource, and probe configuration gaps.

## Safety boundary

This project performs offline, read-only analysis. It does not connect to a Kubernetes API, apply manifests, restart workloads, or execute remediation. Treat output as advisory and validate recommendations against cluster policy and observed production behavior.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Usage

See `app/deployment_review.py` for the public function and its input contract. Import the function and pass parsed Kubernetes data or metric samples as Python dictionaries. Invalid or incomplete input raises `ValueError` rather than silently guessing.

## Tests

Run `pytest` from this directory. Tests cover representative valid input and malformed or boundary input. Tests are included but have not been executed in the remote repository environment.

## Limitations

Rules are deterministic heuristics, not a substitute for Kubernetes API validation, policy-as-code, admission control, workload-specific SLOs, or a production capacity simulation. No model credentials or cluster permissions are required.
