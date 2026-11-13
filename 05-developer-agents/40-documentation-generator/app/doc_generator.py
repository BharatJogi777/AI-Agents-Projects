"""Generate a Markdown module reference from Python AST."""
import ast
def generate(source:str,module_name:str="module")->str:
    if not isinstance(source,str): raise ValueError("source must be text")
    try: tree=ast.parse(source)
    except SyntaxError as exc: raise ValueError(f"Invalid Python source: {exc.msg}") from exc
    lines=[f"# {module_name}","","## Public definitions",""]; found=0
    for node in tree.body:
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and not node.name.startswith("_"):
            kind="Class" if isinstance(node,ast.ClassDef) else "Function"
            doc=ast.get_docstring(node) or "No docstring provided."
            lines.extend(["### "+node.name+" ("+kind+")","",doc,""]); found+=1
    if not found: lines.append("No public top-level classes or functions found.")
    return "\n".join(lines).rstrip()+"\n"
