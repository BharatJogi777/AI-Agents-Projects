import hashlib,mimetypes
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime,timezone
@dataclass(frozen=True)
class DocumentMetadata: name:str; extension:str; media_type:str; size_bytes:int; modified_utc:str; sha256:str
def extract_metadata(path,max_bytes=20000000):
 p=Path(path)
 if p.is_symlink() or not p.is_file(): raise ValueError("expected regular non-symlink file")
 st=p.stat()
 if st.st_size>max_bytes: raise ValueError("file exceeds size limit")
 h=hashlib.sha256()
 with p.open("rb") as f:
  for block in iter(lambda:f.read(65536),b""): h.update(block)
 return DocumentMetadata(p.name,p.suffix.lower(),mimetypes.guess_type(p.name)[0] or "application/octet-stream",st.st_size,datetime.fromtimestamp(st.st_mtime,timezone.utc).isoformat(),h.hexdigest())
