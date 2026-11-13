"""Infer a lightweight module/import graph from Python source files."""
import ast
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class ModuleInfo:
    path: str
    imports: tuple[str, ...]
    classes: tuple[str, ...]
    functions: tuple[str, ...]

def analyze_python_file(path: str | Path, *, root: str | Path | None = None) -> ModuleInfo:
    file = Path(path)
    try:
        source = file.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file))
    except (OSError, UnicodeError, SyntaxError) as exc:
        raise ValueError(f"cannot analyze Python file: {exc}") from exc
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append("." * node.level + (node.module or ""))
    base = Path(root).resolve() if root else file.parent.resolve()
    try:
        display = file.resolve().relative_to(base).as_posix()
    except ValueError:
        display = file.name
    classes = tuple(n.name for n in tree.body if isinstance(n, ast.ClassDef))
    functions = tuple(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
    return ModuleInfo(display, tuple(sorted(set(imports))), classes, functions)

def analyze_tree(root: str | Path, *, max_files: int = 1000) -> tuple[ModuleInfo, ...]:
    base = Path(root).resolve()
    if not base.is_dir() or max_files < 1:
        raise ValueError("root must be a directory and max_files positive")
    paths = sorted(p for p in base.rglob("*.py") if not p.is_symlink() and
                   not set(p.relative_to(base).parts).intersection({".git", ".venv", "__pycache__"}))
    if len(paths) > max_files:
        raise ValueError("Python file limit exceeded")
    return tuple(analyze_python_file(p, root=base) for p in paths)
