"""Flag potentially destructive SQL migration statements for human review."""
import re
RULES=[
("critical",r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b","Destructive object removal"),
("high",r"\bTRUNCATE\b","Removes all rows from a table"),
("high",r"\bALTER\s+TABLE\b[\s\S]*?\bDROP\s+COLUMN\b","Drops a column and may destroy data"),
("medium",r"\bALTER\s+TABLE\b[\s\S]*?\bADD\s+COLUMN\b(?![\s\S]*\bDEFAULT\b)","New column may require backfill or default"),
("medium",r"\bCREATE\s+INDEX\b(?!\s+CONCURRENTLY)","Index creation may block writes depending on database"),
]
def review(sql: str) -> list[dict]:
    if not isinstance(sql,str) or not sql.strip(): raise ValueError("SQL migration must be non-empty")
    findings=[]
    for severity,pattern,message in RULES:
        for match in re.finditer(pattern,sql,re.IGNORECASE):
            line=sql.count("\n",0,match.start())+1
            findings.append({"severity":severity,"line":line,"statement":match.group(0)[:160],"message":message})
    return findings
