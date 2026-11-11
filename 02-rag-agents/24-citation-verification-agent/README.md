# AG-74 — Citation verification agent

Verify that each citation references a known source and that its quoted evidence is an exact substring of that source.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This project is a deterministic component with an injected model/scoring boundary where applicable. Citation checks prove source identity and exact-quote presence, not that a source logically entails a claim. Evidence coverage measures citation presence, not truth. Tests are authored but have not been run locally.
