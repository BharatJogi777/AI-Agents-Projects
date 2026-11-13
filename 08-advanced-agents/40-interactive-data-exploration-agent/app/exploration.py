"""Profile tabular data and produce deterministic exploration suggestions."""
from dataclasses import dataclass
from math import isfinite
from typing import Iterable

@dataclass(frozen=True)
class ColumnProfile:
    name: str
    count: int
    missing: int
    distinct: int
    numeric_min: float | None
    numeric_max: float | None

def profile_table(headers: Iterable[str], rows: Iterable[Iterable[object]]) -> list[ColumnProfile]:
    names = tuple(str(h).strip() for h in headers)
    if not names or any(not n for n in names) or len(set(names)) != len(names):
        raise ValueError("headers must be non-empty and unique")
    columns = [[] for _ in names]
    for row in rows:
        values = list(row)
        if len(values) != len(names):
            raise ValueError("row width does not match headers")
        for bucket, value in zip(columns, values):
            bucket.append(value)
    result = []
    for name, values in zip(names, columns):
        present = [v for v in values if v is not None and str(v).strip() != ""]
        numeric = []
        for value in present:
            try:
                number = float(value)
                if isfinite(number):
                    numeric.append(number)
            except (TypeError, ValueError):
                numeric = []
                break
        result.append(ColumnProfile(name, len(values), len(values)-len(present), len({str(v) for v in present}), min(numeric) if numeric else None, max(numeric) if numeric else None))
    return result

def suggest_explorations(profiles: Iterable[ColumnProfile]) -> list[str]:
    suggestions = []
    for p in profiles:
        if p.missing:
            suggestions.append(f"Inspect missing values in {p.name} ({p.missing}/{p.count}).")
        if p.numeric_min is not None:
            suggestions.append(f"Explore the distribution and outliers of {p.name} ({p.numeric_min} to {p.numeric_max}).")
        if p.distinct <= 20 and p.count:
            suggestions.append(f"Review category frequencies for {p.name} ({p.distinct} distinct values).")
    return suggestions
