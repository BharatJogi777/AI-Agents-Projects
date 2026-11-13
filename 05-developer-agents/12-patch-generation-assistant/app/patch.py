"""Create reviewable unified diffs without modifying source files."""
from __future__ import annotations
import difflib


def generate_patch(original: str, replacement: str, old: str, new: str, *, allow_multiple: bool = False) -> str:
    for name, value in (("original", original), ("replacement", replacement), ("old", old), ("new", new)):
        if not isinstance(value, str):
            raise TypeError(f"{name} must be text")
    if not old:
        raise ValueError("old text must not be empty")
    count = original.count(old)
    if count == 0:
        raise ValueError("expected text was not found")
    if count > 1 and not allow_multiple:
        raise ValueError(f"expected one match, found {count}; set allow_multiple=True explicitly")
    updated = original.replace(old, new) if allow_multiple else original.replace(old, new, 1)
    return "".join(difflib.unified_diff(
        original.splitlines(keepends=True), updated.splitlines(keepends=True),
        fromfile="a/source", tofile="b/source",
    ))


if __name__ == "__main__":
    print(generate_patch("timeout = 5\n", "timeout = 10\n", "timeout = 5", "timeout = 10"))
