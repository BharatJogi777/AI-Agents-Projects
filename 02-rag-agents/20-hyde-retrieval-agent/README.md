# AG-70 — HyDE retrieval agent

Generate a hypothetical document for query expansion while never treating generated text as evidence.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

Generated hypothetical content is used only to shape retrieval queries. It must never be cited as a source or presented as verified evidence. Tests are authored but not locally executed.
