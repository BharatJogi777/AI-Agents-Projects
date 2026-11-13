"""Extract Python definitions and import relationships without executing code."""
import ast
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
    name: str
    kind: str
    line: int
    parent: str | None = None

def extract_symbols(source: str) -> tuple[Symbol, ...]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python syntax at line {exc.lineno}: {exc.msg}") from exc
    found = []
    def visit(nodes, parent=None):
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                found.append(Symbol(node.name, "class", node.lineno, parent))
                visit(node.body, node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                kind = "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function"
                found.append(Symbol(node.name, kind, node.lineno, parent))
    visit(tree.body)
    return tuple(found)

def import_dependencies(source: str) -> tuple[str, ...]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python syntax at line {exc.lineno}: {exc.msg}") from exc
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add("." * node.level + (node.module or ""))
    return tuple(sorted(names))
