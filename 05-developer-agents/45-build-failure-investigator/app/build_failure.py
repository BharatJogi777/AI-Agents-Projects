"""Classify common build-log symptoms into actionable investigation steps."""
RULES=[
("dependency_resolution",["could not resolve","no matching distribution","dependency resolution"],"Check package index, version constraints, and lockfile consistency"),
("compile_error",["syntaxerror","undefined reference","compilation failed","cannot find symbol"],"Inspect the first compiler error and the source location before later cascading errors"),
("missing_tool",["command not found","executable file not found","no such file or directory"],"Verify tool installation, PATH, and build image contents"),
("test_failure",["tests failed","test failed","assertionerror"],"Reproduce the failing test and inspect recent changes and fixtures"),
("permission",["permission denied","operation not permitted"],"Check file ownership, executable bits, and least-privilege build permissions"),
("resource_exhaustion",["out of memory","killed process","no space left on device"],"Inspect memory, disk, and concurrency limits for the build worker"),
]
def investigate(log:str)->dict:
    if not isinstance(log,str) or not log.strip(): raise ValueError("build log must be non-empty")
    lowered=log.lower(); findings=[]
    for category,needles,action in RULES:
        matches=[needle for needle in needles if needle in lowered]
        if matches:
            findings.append({"category":category,"evidence":matches,"next_step":action})
    return {"findings":findings,"primary_category":findings[0]["category"] if findings else None,"summary":"Likely build failure categories found" if findings else "No known signature matched; inspect full logs and build environment"}
