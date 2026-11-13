# Dependency Upgrade Planner

Compares declared current and target dependency versions and produces a staged upgrade checklist. It highlights major-version jumps and missing target versions without accessing package registries or modifying manifests.

## Run
```bash
pip install -e ".[dev]"
python -m app.upgrade
pytest
```

## Limitations
Version comparison follows a conservative numeric semantic-version subset. Pre-releases, local versions, and ecosystem-specific constraints need authoritative tooling and human review.
