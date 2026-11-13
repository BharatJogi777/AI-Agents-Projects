# AWS cost anomaly investigator

Compare daily service costs with a historical baseline and explain significant increases without making billing or resource changes.

## Safety boundary

This project analyzes supplied snapshots only. It does not connect to AWS, change infrastructure, delete resources, or apply remediation. Validate findings against live provider APIs and organizational policy before acting.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Input and behavior

See the public function in `app/cost_anomaly.py`. Inputs are validated and findings retain resource or statement evidence. Unknown or incomplete data should be investigated rather than treated as proof of safety.

## Limitations

The analyzer is deterministic and provider-data-format dependent. It is a triage aid, not a complete cloud security scanner or authoritative billing/network diagnosis. No cloud credentials are required.
