# TypeScript code review assistant

## Purpose
A focused static-analysis assistant that highlights review risks from supplied source or structured observations. It does not modify code or execute user input.

## Run
```bash
python -m pip install -e '.[dev]'
pytest
```

## API
See `app/typescript_review.py` for the public function and finding schema. Invalid inputs raise `ValueError`.

## Limitations and safety
These checks are heuristics and may produce false positives or miss context-dependent bugs. Use the language compiler, race detector, profiler, tests, and human review as appropriate before merging changes.
