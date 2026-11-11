import json
from dataclasses import dataclass
@dataclass(frozen=True)
class JSONRecord: path:str; canonical_json:str
def parse_json_records(source:str|bytes,max_bytes:int=5000000,max_records:int=100000)->list[JSONRecord]:
 raw=source.encode() if isinstance(source,str) else source
 if not isinstance(raw,bytes): raise TypeError("source must be str or bytes")
 if len(raw)>max_bytes: raise ValueError("JSON too large")
 def reject(value): raise ValueError(f"invalid JSON constant: {value}")
 data=json.loads(raw,parse_constant=reject)
 if isinstance(data,list): items=[(f"$[{i}]",v) for i,v in enumerate(data)]
 elif isinstance(data,dict): items=[("$",data)]
 else: raise ValueError("top-level JSON must be object or array")
 if len(items)>max_records: raise ValueError("too many records")
 return [JSONRecord(path,json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False)) for path,v in items]
