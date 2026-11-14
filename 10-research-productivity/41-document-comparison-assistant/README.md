# AG-491: Document comparison assistant

Compare two supplied document versions by normalized lines and report additions, removals, and unchanged content.

## Scope

A deterministic Python reference implementation operating only on caller-supplied data. It does not contact external services, submit proposals, or make commitments on behalf of an organization.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Review and safety

Outputs are drafts or screening results, not verified facts or professional approvals. Confirm source material, eligibility, deadlines, and all final content with the responsible human owner. Tests are authored but have not been executed in this repository workflow.
