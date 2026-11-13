"""Classify common static type-checker diagnostics."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class TypeDiagnosis:
    category: str
    message: str
    likely_cause: str
    next_steps: tuple[str, ...]


RULES = (
    (("optional", "possibly none", "none is not"), "optional-value", "A value may be None where a concrete value is required"),
    (("incompatible type", "incompatible assignment"), "assignment", "The assigned expression does not match the declared type"),
    (("has no attribute", "unknown member"), "missing-attribute", "The declared type does not expose the accessed attribute"),
    (("missing positional argument", "unexpected keyword", "too many arguments"), "call-signature", "The call does not match the function signature"),
)


def diagnose(messages: list[str]) -> list[TypeDiagnosis]:
    if not isinstance(messages, list) or any(not isinstance(x, str) or not x.strip() for x in messages):
        raise ValueError("messages must be a list of non-empty strings")
    results = []
    for message in messages:
        lowered = message.lower()
        match = next(((category, cause) for terms, category, cause in RULES if any(t in lowered for t in terms)), None)
        category, cause = match if match else ("unclassified", "The diagnostic requires inspection in its original checker context")
        results.append(TypeDiagnosis(category, message, cause, (
            "Inspect the inferred and declared types at the reported location",
            "Prefer correcting the data flow or contract over adding an unsafe cast",
            "Add a focused type-checking regression example",
        )))
    return results


def to_json(items: list[TypeDiagnosis]) -> str:
    return json.dumps([asdict(x) for x in items], indent=2)


if __name__ == "__main__":
    print(to_json(diagnose(["Argument has incompatible type str; expected int"])))
