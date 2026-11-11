import hashlib,re
from dataclasses import dataclass
@dataclass(frozen=True)
class DuplicateGroup: digest:str; document_ids:tuple[str,...]
def normalize(text): return " ".join(re.findall(r"\w+",text.casefold()))
def deduplicate(documents):
 buckets={}
 for doc_id,text in documents.items():
  if not doc_id or not isinstance(text,str): raise ValueError("document ID and text required")
  digest=hashlib.sha256(normalize(text).encode()).hexdigest(); buckets.setdefault(digest,[]).append(doc_id)
 return [DuplicateGroup(k,tuple(v)) for k,v in sorted(buckets.items()) if len(v)>1]
