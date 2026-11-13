# Smart home routine planner

Deterministic Python reference implementation for **AG-395**. It converts explicitly supplied inputs into reviewable plans and does not connect to dashboards, mobile devices, desktop applications, IoT hardware, or home automation services.

## Run

```bash
python -m pytest
```

## Safety boundaries

- Uses explicit allowlists and validates requested operations.
- Produces plans or findings; it does not execute device or system actions.
- State-changing actions require an explicit approval step in the calling application.
