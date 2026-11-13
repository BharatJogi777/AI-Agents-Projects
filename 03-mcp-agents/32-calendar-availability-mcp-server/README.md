# AG-132 — Calendar availability MCP server

A pure availability calculator that subtracts busy events from a timezone-aware search window and merges overlapping events.

## Run
```bash
pip install -e '.[dev]'
pytest
```

The MCP adapter should fetch events using a read-only calendar scope, normalize all timestamps to aware datetimes, and return only free intervals. Enforce calendar ownership and avoid exposing event titles, attendees, or descriptions when calculating availability.

## Limitations
This module does not connect to Google/Microsoft calendars and does not handle recurrence expansion, working hours, travel buffers, or daylight-saving recurrence rules. Those belong in a provider adapter and timezone-aware scheduling layer.
