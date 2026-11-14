"""Compare two supplied text versions without changing either source."""
from difflib import SequenceMatcher

def compare_documents(before: str, after: str) -> dict:
    if not isinstance(before, str) or not isinstance(after, str):
        raise ValueError("documents must be strings")
    if not before.strip() or not after.strip():
        raise ValueError("both documents must contain text")
    left, right = before.splitlines(), after.splitlines()
    matcher = SequenceMatcher(a=left, b=right, autojunk=False)
    changes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            changes.append({"kind": tag, "before": left[i1:i2], "after": right[j1:j2], "before_lines": [i1+1, i2], "after_lines": [j1+1, j2]})
    return {"added_lines": sum(len(c["after"]) for c in changes if c["kind"] in ("insert","replace")), "removed_lines": sum(len(c["before"]) for c in changes if c["kind"] in ("delete","replace")), "changes": changes}
