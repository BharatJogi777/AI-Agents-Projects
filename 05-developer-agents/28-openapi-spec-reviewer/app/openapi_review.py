"""Review core OpenAPI document structure without silently rewriting it."""
def review(spec: dict) -> list[dict]:
    if not isinstance(spec,dict): raise ValueError("OpenAPI document must be an object")
    findings=[]
    version=spec.get("openapi")
    if not isinstance(version,str) or not version.startswith("3."): findings.append({"severity":"error","path":"openapi","message":"Expected an OpenAPI 3.x version"})
    info=spec.get("info")
    if not isinstance(info,dict): findings.append({"severity":"error","path":"info","message":"Required info object is missing"})
    else:
        for key in ("title","version"):
            if not isinstance(info.get(key),str) or not info[key].strip(): findings.append({"severity":"error","path":f"info.{key}","message":f"Required non-empty {key}"})
    paths=spec.get("paths")
    if not isinstance(paths,dict) or not paths: findings.append({"severity":"error","path":"paths","message":"At least one path is required"})
    else:
        for path, item in paths.items():
            if not isinstance(path,str) or not path.startswith("/"): findings.append({"severity":"error","path":f"paths.{path}","message":"Path must start with /"})
            if not isinstance(item,dict): findings.append({"severity":"error","path":f"paths.{path}","message":"Path item must be an object"}); continue
            for method, operation in item.items():
                if method.lower() not in {"get","put","post","delete","options","head","patch","trace","parameters","$ref","summary","description","servers"}: continue
                if method.lower() in {"get","put","post","delete","options","head","patch","trace"}:
                    if not isinstance(operation,dict): findings.append({"severity":"error","path":f"paths.{path}.{method}","message":"Operation must be an object"}); continue
                    if not operation.get("responses"): findings.append({"severity":"error","path":f"paths.{path}.{method}.responses","message":"Operation must declare responses"})
                    if not operation.get("operationId"): findings.append({"severity":"warning","path":f"paths.{path}.{method}.operationId","message":"Stable operationId is recommended"})
    return findings
