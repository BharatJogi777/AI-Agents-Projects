"""Static heuristics for SQL query review; not a query planner."""
import re
def review(sql: str) -> list[dict]:
    if not isinstance(sql,str) or not sql.strip(): raise ValueError("SQL must be non-empty")
    findings=[]
    rules=[
      (r"SELECT\s+\*", "warning", "Avoid SELECT * when a stable, narrow projection is possible"),
      (r"\bNOT\s+IN\s*\(", "warning", "Check NULL semantics; NOT EXISTS may be safer"),
      (r"\bLIKE\s+['\"]%", "info", "Leading wildcard can prevent ordinary B-tree index use"),
      (r"\bOFFSET\s+\d+", "info", "Large OFFSET pagination can become expensive"),
      (r"\bUPDATE\b(?![\s\S]*\bWHERE\b)", "critical", "UPDATE without WHERE may affect every row"),
      (r"\bDELETE\s+FROM\b(?![\s\S]*\bWHERE\b)", "critical", "DELETE without WHERE may remove every row"),
    ]
    for pattern,severity,message in rules:
      for m in re.finditer(pattern,sql,re.IGNORECASE):
        findings.append({"severity":severity,"line":sql.count("\n",0,m.start())+1,"message":message})
    return findings
