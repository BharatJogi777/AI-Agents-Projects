"""Extract structured test failures and cautious diagnostic suggestions."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
import re


@dataclass(frozen=True)
class Diagnosis:
    kind: str
    location: str | None
    message: str
    evidence: str
    suggestions: tuple[str, ...]


def diagnose_output(output: str) -> list[Diagnosis]:
    if not isinstance(output, str):
        raise TypeError("output must be text")
    results = []
    for line in output.splitlines():
        match = re.match(r"^(.+?\.py:\d+):\s*(.+)$", line.strip())
        if not match:
            continue
        location, message = match.groups()
        lowered = message.lower()
        if "assert" in lowered:
            kind, suggestions = "assertion", ("Compare expected and actual values", "Check fixture data and boundary conditions")
        elif "modulenotfounderror" in lowered or "importerror" in lowered:
            kind, suggestions = "import", ("Verify the active interpreter and installed dependencies", "Check package and module paths")
        elif "error" in lowered:
            kind, suggestions = "runtime", ("Inspect the complete traceback and failing input", "Check recent changes to the failing code path")
        else:
            kind, suggestions = "test-failure", ("Inspect the complete failure context", "Re-run the individual test to confirm reproducibility")
        results.append(Diagnosis(kind, location, message, line.strip()[:500], suggestions))
    if not results and output.strip():
        results.append(Diagnosis("unclassified", None, "No recognized pytest failure location", output.strip()[-1000:],
                                 ("Retain and inspect the complete test log", "Check collection and setup output for earlier errors")))
    return results


def to_json(results: list[Diagnosis]) -> str:
    return json.dumps([asdict(item) for item in results], indent=2)


if __name__ == "__main__":
    print(to_json(diagnose_output("tests/test_api.py:12: AssertionError: expected 200")))
