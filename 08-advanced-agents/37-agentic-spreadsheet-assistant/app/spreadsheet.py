"""Safely inspect tabular data and preview edits without executing spreadsheet formulas."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Sheet:
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

@dataclass(frozen=True)
class Preview:
    row_index: int
    column: str
    old_value: str
    new_value: str

def validate_sheet(headers: Iterable[str], rows: Iterable[Iterable[object]]) -> Sheet:
    names = tuple(str(h).strip() for h in headers)
    if not names or any(not h for h in names) or len(set(names)) != len(names):
        raise ValueError("headers must be non-empty and unique")
    normalized = []
    for row in rows:
        values = tuple("" if v is None else str(v) for v in row)
        if len(values) != len(names):
            raise ValueError("every row must match header width")
        normalized.append(values)
    return Sheet(names, tuple(normalized))

def preview_replace(sheet: Sheet, *, column: str, old: str, new: str) -> list[Preview]:
    if column not in sheet.headers:
        raise KeyError(column)
    if not old:
        raise ValueError("old value must not be empty")
    index = sheet.headers.index(column)
    previews = []
    for row_index, row in enumerate(sheet.rows):
        if old in row[index]:
            previews.append(Preview(row_index, column, row[index], row[index].replace(old, new)))
    return previews

def csv_safe_cell(value: object) -> str:
    """Prefix formula-like text so spreadsheet applications treat it as data."""
    text = "" if value is None else str(value)
    if text.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + text
    return text
