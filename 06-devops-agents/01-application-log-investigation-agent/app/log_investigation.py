"""Read-only log grouping and investigation summary."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class LogFinding:
    signature: str
    count: int
    first_line: int
    last_line: int

def investigate_logs(log_text: str, *, max_lines: int = 10000) -> list[LogFinding]:
    if not isinstance(log_text, str): raise TypeError("log_text must be a string")
    if not 1 <= max_lines <= 100000: raise ValueError("max_lines must be between 1 and 100000")
    all_lines=log_text.splitlines()
    offset=max(0,len(all_lines)-max_lines)
    lines=all_lines[-max_lines:]
    positions={}
    for number,line in enumerate(lines,start=offset+1):
        if not line.strip(): continue
        normalized=re.sub(r"\b[0-9a-f]{8,}\b","<id>",line.lower())
        normalized=re.sub(r"\b\d+\b","<n>",normalized)
        key=normalized[:240]
        if key not in positions: positions[key]=[0,number,number]
        positions[key][0]+=1; positions[key][2]=number
    return [LogFinding(k,v[0],v[1],v[2]) for k,v in sorted(positions.items(),key=lambda item:(-item[1][0],item[0]))]
