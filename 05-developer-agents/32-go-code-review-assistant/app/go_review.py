"""Conservative text-based checks for common Go code review risks."""
import re
def review(source: str) -> list[dict]:
    if not isinstance(source,str) or not source.strip(): raise ValueError("Go source must be non-empty")
    findings=[]
    checks=[
      (r"\bpanic\s*\(", "warning", "Check whether panic is appropriate in this execution path"),
      (r"\bgo\s+func\s*\(", "warning", "Review goroutine lifecycle, cancellation, and error propagation"),
      (r"\bhttp\.DefaultClient\b", "warning", "Use a client with explicit timeout policy for outbound requests"),
      (r"\bcontext\.Background\s*\(\)", "info", "Confirm this root context is not discarding a caller deadline"),
      (r"\bdefer\s+\w+\.Close\s*\(\)", "info", "Consider handling close errors when they can affect correctness"),
    ]
    for pattern,severity,message in checks:
      for m in re.finditer(pattern,source):
        findings.append({"severity":severity,"line":source.count("\n",0,m.start())+1,"message":message})
    return findings
