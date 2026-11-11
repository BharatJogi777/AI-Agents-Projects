from dataclasses import dataclass
import hashlib
@dataclass(frozen=True)
class ChildChunk: id:str; parent_id:str; text:str; start:int; end:int
@dataclass(frozen=True)
class ParentChunk: id:str; text:str
def build_parent_child(document_id,text,parent_chars=2000,child_chars=400):
 if not document_id or parent_chars<child_chars or child_chars<1: raise ValueError("invalid IDs or chunk sizes")
 parents=[]; children=[]
 for start in range(0,len(text),parent_chars):
  part=text[start:start+parent_chars]; pid=hashlib.sha256(f"{document_id}:p:{start}".encode()).hexdigest(); parents.append(ParentChunk(pid,part))
  for ci,off in enumerate(range(0,len(part),child_chars)):
   child=part[off:off+child_chars]; cid=hashlib.sha256(f"{pid}:c:{ci}".encode()).hexdigest(); children.append(ChildChunk(cid,pid,child,start+off,start+off+len(child)))
 return parents,children
def expand_to_parents(child_ids,children,parents):
 cmap={c.id:c for c in children}; pmap={p.id:p for p in parents}; seen=set(); out=[]
 for cid in child_ids:
  c=cmap.get(cid)
  if c and c.parent_id in pmap and c.parent_id not in seen: seen.add(c.parent_id); out.append(pmap[c.parent_id])
 return out
