"""Turn conflict metadata into a cautious manual resolution checklist."""
def guide(files:list[dict])->list[dict]:
    result=[]
    actions={
      "content":["Inspect both versions and surrounding history","Resolve intent manually; preserve required behavior","Run focused tests and inspect final diff"],
      "rename":["Confirm intended destination path","Check imports, references, and build manifests","Verify no duplicate or missing files remain"],
      "delete_modify":["Determine whether deletion or modification is intentional","Check callers and deployment references","Do not restore or delete without owner confirmation"],
      "binary":["Identify authoritative binary version","Avoid line-based merge tools","Validate resulting artifact opens correctly"],
    }
    for item in files:
        path=item.get("path"); kind=item.get("kind","content")
        if not isinstance(path,str) or not path.strip(): raise ValueError("each conflict requires a path")
        if kind not in actions: raise ValueError("unsupported conflict kind")
        result.append({"path":path,"kind":kind,"steps":actions[kind],"requires_human_decision":kind in {"delete_modify","binary"}})
    return result
