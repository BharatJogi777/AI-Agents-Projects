# Autonomous workflow sandbox

Deterministic Python reference implementation for **AG-400**. The implementation creates a constrained plan or simulation result from supplied data. It does not connect to physical robots, games, simulation infrastructure, or digital-twin services.

## Run

```bash
python -m pytest
```

## Safety boundaries

- Validates operations and resource bounds before planning.
- Keeps execution separate from planning where external side effects could occur.
- Uses explicit registered functions and caller-supplied data only.
