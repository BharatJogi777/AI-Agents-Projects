# Incident postmortem drafter

Turn structured incident facts into a blameless postmortem draft while clearly separating confirmed facts from hypotheses.

## Safety boundary

This tool operates only on supplied metadata and creates plans or assessments. It never reads secret values, installs patches, changes cloud resources, certifies production readiness, or invents incident facts. Operational changes require accountable owner review and approval.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Validate inventory completeness, policy baselines, cost assumptions, and incident evidence before relying on the output.
