"""AST-backed checks for selected Python correctness and maintainability risks."""
import ast
def review(source: str) -> list[dict]:
    if not isinstance(source,str) or not source.strip(): raise ValueError("Python source must be non-empty")
    try: tree=ast.parse(source)
    except SyntaxError as exc: return [{"severity":"error","line":exc.lineno or 1,"message":f"Syntax error: {exc.msg}"}]
    findings=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.ExceptHandler) and node.type is None:
            findings.append({"severity":"warning","line":node.lineno,"message":"Bare except catches BaseException; catch narrower exceptions"})
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
            for default in node.args.defaults + node.args.kw_defaults:
                if isinstance(default,(ast.List,ast.Dict,ast.Set)):
                    findings.append({"severity":"high","line":node.lineno,"message":f"Mutable default argument in {node.name}"})
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="eval":
            findings.append({"severity":"high","line":node.lineno,"message":"eval executes dynamic code; avoid untrusted input"})
    return findings
