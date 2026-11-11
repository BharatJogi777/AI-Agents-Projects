# AG-69 — Multi-query retrieval agent

Retrieve across query variants, deduplicate candidates, and fuse ranks using reciprocal rank fusion.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

Generated hypothetical content is used only to shape retrieval queries. It must never be cited as a source or presented as verified evidence. Tests are authored but not locally executed.
