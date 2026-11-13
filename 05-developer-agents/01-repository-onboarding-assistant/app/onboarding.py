"""Build a safe, concise onboarding inventory from a repository directory."""
from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDES = {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}

@dataclass(frozen=True)
class RepositoryInventory:
    root: str
    files: tuple[str, ...]
    directories: tuple[str, ...]
    entrypoints: tuple[str, ...]
    manifests: tuple[str, ...]

def inspect_repository(root: str | Path, *, max_files: int = 5000) -> RepositoryInventory:
    base = Path(root).expanduser().resolve()
    if not base.exists() or not base.is_dir():
        raise ValueError("repository root must be an existing directory")
    if max_files < 1:
        raise ValueError("max_files must be positive")
    files, dirs = [], set()
    for path in sorted(base.rglob("*")):
        rel = path.relative_to(base)
        if any(part in DEFAULT_EXCLUDES for part in rel.parts):
            continue
        if path.is_symlink():
            continue
        if path.is_dir():
            dirs.add(rel.as_posix())
        elif path.is_file():
            files.append(rel.as_posix())
            if len(files) > max_files:
                raise ValueError(f"repository exceeds max_files={max_files}")
    manifests = tuple(p for p in files if Path(p).name in {
        "pyproject.toml", "package.json", "go.mod", "Cargo.toml", "pom.xml", "requirements.txt"
    })
    entrypoints = tuple(p for p in files if Path(p).name in {
        "main.py", "app.py", "main.go", "server.js", "index.js", "main.ts"
    })
    return RepositoryInventory(str(base), tuple(files), tuple(sorted(dirs)), entrypoints, manifests)
