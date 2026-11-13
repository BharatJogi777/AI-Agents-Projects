"""Create audience-friendly release notes from categorized changes."""
def create_release_notes(version:str,changes:list[dict],audience:str="users")->str:
    if not isinstance(version,str) or not version.strip(): raise ValueError("version is required")
    if audience not in {"users","developers","internal"}: raise ValueError("unsupported audience")
    sections={"Added":[],"Changed":[],"Fixed":[],"Security":[]}
    for item in changes:
        category=item.get("category"); description=item.get("description")
        if category not in sections: raise ValueError(f"unsupported category: {category!r}")
        if not isinstance(description,str) or not description.strip(): raise ValueError("description is required")
        text=description.strip()
        if audience=="users" and item.get("internal_only",False): continue
        sections[category].append(text)
    lines=["# Release "+version.strip(),""]
    for category,items in sections.items():
        if items:
            lines.extend(["## "+category,""])
            lines.extend("- "+x for x in items); lines.append("")
    if len(lines)==3: lines.append("No user-facing changes recorded.")
    return "\n".join(lines).rstrip()+"\n"
