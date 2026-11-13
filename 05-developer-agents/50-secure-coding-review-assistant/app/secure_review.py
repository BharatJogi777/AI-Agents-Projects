"""Conservative static security checks for Python source."""
import ast
from dataclasses import dataclass

@dataclass(frozen=True)
class Finding:
    rule: str
    line: int
    message: str

def review_source(source: str) -> list[Finding]:
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python syntax at line {exc.lineno}: {exc.msg}") from exc
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        dotted = (func.value.id + "." + func.attr) if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) else (func.id if isinstance(func, ast.Name) else "")
        if dotted in {"eval", "exec"}:
            findings.append(Finding("dynamic-execution", node.lineno, "Dynamic code execution can run untrusted input."))
        if dotted in {"pickle.loads", "marshal.loads"}:
            findings.append(Finding("unsafe-deserialization", node.lineno, "Deserializing untrusted serialized data can execute code or instantiate unsafe objects."))
        if dotted.startswith("subprocess.") and any(k.arg == "shell" and isinstance(k.value, ast.Constant) and k.value.value is True for k in node.keywords):
            findings.append(Finding("shell-injection", node.lineno, "shell=True requires strict command and argument controls."))
        if dotted.endswith(".execute") and node.args and isinstance(node.args[0], ast.JoinedStr):
            findings.append(Finding("sql-interpolation", node.lineno, "SQL f-string interpolation may permit injection; use parameterized queries."))
    return sorted(findings, key=lambda f: (f.line, f.rule))
