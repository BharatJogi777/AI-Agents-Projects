# Helm values reviewer

## Purpose

Review a parsed Helm values document for common production readiness gaps without rendering or applying a chart.

## Safety

Offline, read-only analysis only. No Docker daemon, Kubernetes cluster, Helm release, Terraform backend, or cloud credentials are accessed. Findings are advisory and require human review.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Usage

Import `review_values` from `app.helm_review` and pass the documented Python dictionary/list input. Invalid structures raise `ValueError`.

## Tests and limitations

Run `pytest`. Tests are included for representative behavior and invalid input but have not been executed in the remote repository environment. This is a deterministic heuristic, not a replacement for native tooling or policy-as-code.
