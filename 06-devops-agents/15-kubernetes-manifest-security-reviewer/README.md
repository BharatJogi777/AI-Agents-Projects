# Kubernetes manifest security reviewer

## Purpose

Perform offline security checks on Kubernetes workload manifests and report actionable findings with severity and remediation guidance.

## Safety boundary

This project performs offline, read-only analysis. It does not connect to a Kubernetes API, apply manifests, restart workloads, or execute remediation. Treat output as advisory and validate recommendations against cluster policy and production requirements.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Usage

Import `review_manifests` from `app.manifest_security` and pass a list of parsed Kubernetes manifest dictionaries. Findings include severity, rule code, resource name, and remediation guidance. Invalid documents raise `ValueError`.

## Tests

Run `pytest` from this directory. Tests cover security findings and malformed input. Tests are authored but have not been executed in the remote repository environment.

## Limitations

This is a focused static heuristic, not a complete Kubernetes benchmark or admission controller. It does not resolve Pod Security Standards, custom policies, RBAC, network policies, image provenance, mounted secrets, or cluster-specific exceptions. No cluster credentials or model API keys are required.
