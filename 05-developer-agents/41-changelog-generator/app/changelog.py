"""Group conventional commits into a deterministic Markdown changelog."""
import re
PATTERN=re.compile(r"^(feat|fix|docs|refactor|perf|test|build|ci|chore)(?:\([^)]*\))?(!)?:\s+(.+)$")
SECTIONS={"feat":"Features","fix":"Bug fixes","perf":"Performance","docs":"Documentation","refactor":"Refactoring","test":"Tests","build":"Build","ci":"CI","chore":"Maintenance"}
def generate(commits:list[str],version:str)->str:
    if not isinstance(version,str) or not version.strip(): raise ValueError("version is required")
    groups={key:[] for key in SECTIONS}
    for commit in commits:
        if not isinstance(commit,str): raise ValueError("commit messages must be strings")
        match=PATTERN.match(commit.strip())
        if match:
            kind,breaking,subject=match.groups()
            prefix="**BREAKING:** " if breaking else ""
            groups[kind].append(prefix+subject.strip())
    lines=["# "+version.strip(),""]; count=0
    for key,title in SECTIONS.items():
        if groups[key]:
            lines.extend(["## "+title,""])
            lines.extend("- "+item for item in groups[key]); lines.append(""); count+=len(groups[key])
    if not count: lines.append("No conventional commits found.")
    return "\n".join(lines).rstrip()+"\n"
