"""Search source repositories with bounded, literal or regex matching."""
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass(frozen=True)
class Match:
    path: str
    line: int
    text: str

def search_code(root: str | Path, query: str, *, regex: bool = False,
                suffixes: tuple[str, ...] = (".py", ".go", ".js", ".ts", ".java"),
                max_matches: int = 200, max_file_bytes: int = 1_000_000) -> list[Match]:
    base = Path(root).resolve()
    if not base.is_dir() or not query or max_matches < 1 or max_file_bytes < 1:
        raise ValueError("valid directory, query, and positive limits are required")
    try:
        pattern = re.compile(query if regex else re.escape(query))
    except re.error as exc:
        raise ValueError(f"invalid search regex: {exc}") from exc
    matches = []
    for path in sorted(base.rglob("*")):
        rel = path.relative_to(base)
        if path.is_symlink() or not path.is_file() or path.suffix not in suffixes:
            continue
        if set(rel.parts).intersection({".git", ".venv", "node_modules", "__pycache__"}):
            continue
        try:
            if path.stat().st_size > max_file_bytes:
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(lines, 1):
            if pattern.search(line):
                matches.append(Match(rel.as_posix(), number, line.strip()))
                if len(matches) >= max_matches:
                    return matches
    return matches
