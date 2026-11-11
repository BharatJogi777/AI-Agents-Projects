import hashlib,json
from typing import Any
class InvalidAgentState(ValueError): pass
def fingerprint_state(state:Any,*,max_bytes:int=64000)->str:
    if not 128<=max_bytes<=1000000: raise ValueError("max_bytes must be 128..1000000")
    try: encoded=json.dumps(state,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    except (TypeError,ValueError) as exc: raise InvalidAgentState("state must contain JSON-compatible finite values") from exc
    if len(encoded)>max_bytes: raise InvalidAgentState("state exceeds fingerprint size limit")
    return hashlib.sha256(encoded).hexdigest()
