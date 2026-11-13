"""Summarize a unified diff into review-oriented change statistics."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class FileChange:
    path: str
    additions: int
    deletions: int
    binary: bool = False

@dataclass(frozen=True)
class PullRequestSummary:
    files: tuple[FileChange, ...]
    additions: int
    deletions: int
    changed_files: int

def summarize_diff(diff: str) -> PullRequestSummary:
    if not isinstance(diff, str):
        raise TypeError("diff must be text")
    files: list[FileChange] = []
    current = None
    adds = dels = 0
    binary = False
    def flush():
        nonlocal current, adds, dels, binary
        if current is not None:
            files.append(FileChange(current, adds, dels, binary))
        current, adds, dels, binary = None, 0, 0, False
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            flush()
            match = re.match(r"diff --git a/(.*?) b/(.*)", line)
            if match: current = match.group(2)
        elif line.startswith("+++ b/"):
            current = line[6:]
        elif line.startswith("Binary files "):
            binary = True
        elif line.startswith("+") and not line.startswith("+++"):
            adds += 1
        elif line.startswith("-") and not line.startswith("---"):
            dels += 1
    flush()
    return PullRequestSummary(tuple(files), sum(f.additions for f in files), sum(f.deletions for f in files), len(files))
