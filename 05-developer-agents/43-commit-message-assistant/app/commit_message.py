"""Draft a conventional commit message from structured change metadata."""
ALLOWED={"feat","fix","docs","refactor","perf","test","build","ci","chore"}
def draft(kind:str,summary:str,scope:str|None=None,breaking:bool=False,body:str|None=None)->str:
    if kind not in ALLOWED: raise ValueError("unsupported conventional commit type")
    if not isinstance(summary,str) or not summary.strip(): raise ValueError("summary is required")
    if scope is not None and (not scope.strip() or any(c in scope for c in "()\n")): raise ValueError("invalid scope")
    header=kind+(f"({scope.strip()})" if scope else "")+("!" if breaking else "")+": "+summary.strip()
    if len(header)>72: raise ValueError("header exceeds 72 characters")
    if body is not None and not isinstance(body,str): raise ValueError("body must be text")
    return header+("\n\n"+body.strip() if body and body.strip() else "")
