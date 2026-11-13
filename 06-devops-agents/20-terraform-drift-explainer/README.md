# Terraform drift explainer

## Purpose

Compare normalized Terraform desired and observed resource attributes, summarize drift, and flag sensitive attribute changes.

## Safety

Offline, read-only analysis only. No Terraform backend, cloud credentials, plan approval, or apply operation is used. Findings are advisory and require human review.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Usage

Import `explain_drift` from `app.terraform_drift` and pass parsed Terraform JSON/state dictionaries. Invalid input raises `ValueError`.

## Tests and limitations

Run `pytest`. Tests cover representative behavior and invalid input but have not been executed in the remote repository environment. This is a deterministic review aid, not a replacement for Terraform validation, policy-as-code, or security review.
