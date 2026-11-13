# Backup verification assistant

Evaluate backup inventory for freshness, integrity checks, restore-test recency, and coverage gaps.

## Safety boundary

This is deterministic decision support over user-supplied evidence. It does not access production systems, change traffic, roll back releases, restore backups, or run disaster-recovery drills. Human owners must validate findings and approve operational actions.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Results are only as reliable as the supplied metrics, dependency map, backup metadata, and objectives. Validate thresholds and runbooks for each environment.
