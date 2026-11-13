"""Explain structured log distributions against a caller-provided baseline."""
import json
from collections import Counter

def explain_anomalies(records: list[dict], baseline: dict[str,float], *, minimum_count: int = 3) -> list[dict]:
    if minimum_count < 1: raise ValueError("minimum_count must be positive")
    counts=Counter()
    for i,record in enumerate(records):
        if not isinstance(record,dict): raise TypeError(f"record {i} must be an object")
        level=str(record.get("level","unknown")).lower()
        counts[level]+=1
    total=sum(counts.values())
    findings=[]
    for level,count in sorted(counts.items()):
        observed=count/total if total else 0.0
        expected=baseline.get(level)
        if expected is not None and (not isinstance(expected,(int,float)) or not 0 <= expected <= 1):
            raise ValueError(f"baseline for {level} must be between 0 and 1")
        if count >= minimum_count and expected is not None and observed > max(expected*2, expected+0.1):
            findings.append({"level":level,"count":count,"observed_rate":observed,"baseline_rate":expected,"explanation":f"{level} logs are elevated relative to the supplied baseline."})
    return findings

def parse_json_lines(text: str, *, max_bytes: int = 1_000_000) -> list[dict]:
    if not isinstance(text,str): raise TypeError("text must be a string")
    if len(text.encode("utf-8")) > max_bytes: raise ValueError("input exceeds max_bytes")
    result=[]
    for line_no,line in enumerate(text.splitlines(),1):
        if not line.strip(): continue
        try: value=json.loads(line)
        except json.JSONDecodeError as exc: raise ValueError(f"invalid JSON on line {line_no}") from exc
        if not isinstance(value,dict): raise ValueError(f"line {line_no} must contain a JSON object")
        result.append(value)
    return result
