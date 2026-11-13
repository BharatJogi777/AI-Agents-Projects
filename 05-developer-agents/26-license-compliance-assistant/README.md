# License compliance assistant

## Purpose
A focused, deterministic developer-assistance utility. It analyzes supplied inputs and returns review findings; it does not silently modify production systems.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## API
See `app/license_audit.py` for the typed, side-effect-limited public functions. Invalid inputs raise `ValueError`. Findings are advisory and must be validated by an engineer before changes are applied.

## Safety and limitations
This project uses static heuristics, not a full compiler, legal opinion, SQL engine, or runtime contract probe. Validate results against authoritative source data and review high-impact findings manually.
