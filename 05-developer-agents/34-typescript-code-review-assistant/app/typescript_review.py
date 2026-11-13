"""Conservative regex checks for selected TypeScript risks."""
import re
def review(source: str) -> list[dict]:
    if not isinstance(source,str) or not source.strip(): raise ValueError("TypeScript source must be non-empty")
    findings=[]
    checks=[
      (r"\bany\b","warning","Replace any with a narrower type where practical"),
      (r"@ts-ignore","warning","Prefer @ts-expect-error with a documented reason"),
      (r"\bJSON\.parse\s*\(","info","Validate parsed data; JSON.parse returns untrusted runtime data"),
      (r"\b as unknown as ","warning","Double assertion bypasses type checking; document invariant"),
      (r"\bPromise\.all\s*\(","info","Consider partial-failure behavior and concurrency limits"),
    ]
    for pattern,message_severity,message in checks:
      for m in re.finditer(pattern,source):
        findings.append({"severity":message_severity,"line":source.count("\n",0,m.start())+1,"message":message})
    return findings
