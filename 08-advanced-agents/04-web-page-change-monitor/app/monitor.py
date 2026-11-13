from dataclasses import dataclass
import hashlib
@dataclass(frozen=True)
class Snapshot:
    url:str
    content:str
    captured_at:str
def fingerprint(s:Snapshot)->str:
    if not s.url.startswith("https://") or not s.content or not s.captured_at: raise ValueError("HTTPS URL, content, and capture timestamp are required")
    return hashlib.sha256(s.content.encode("utf-8")).hexdigest()
def compare(previous:Snapshot|None,current:Snapshot)->dict:
    new=fingerprint(current)
    if previous is None: return {"status":"baseline","changed":False,"fingerprint":new}
    if previous.url!=current.url: raise ValueError("cannot compare snapshots from different URLs")
    old=fingerprint(previous)
    return {"status":"changed" if old!=new else "unchanged","changed":old!=new,"previous":old,"current":new}
