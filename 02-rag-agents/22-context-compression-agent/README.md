# AG-72 — Context compression agent

Select relevant exact source sentences under a character budget while retaining document IDs and source offsets.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This project is a deterministic component with an injected model/scoring boundary where applicable. Citation checks prove source identity and exact-quote presence, not that a source logically entails a claim. Evidence coverage measures citation presence, not truth. Tests are authored but have not been run locally.
