import hashlib,sqlite3
from pathlib import Path
class IncrementalIndexer:
 def __init__(self,db_path:str|Path,chunk_chars:int=1000,overlap:int=100):
  if chunk_chars<100 or overlap<0 or overlap>=chunk_chars: raise ValueError("invalid chunk sizing")
  self.db=sqlite3.connect(str(db_path)); self.db.execute("PRAGMA foreign_keys=ON"); self.chunk_chars=chunk_chars; self.overlap=overlap
  self.db.executescript("CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY, content_hash TEXT NOT NULL); CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY, document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE, ordinal INTEGER NOT NULL, start_offset INTEGER NOT NULL, end_offset INTEGER NOT NULL, text TEXT NOT NULL, UNIQUE(document_id,ordinal));")
 def close(self): self.db.close()
 def index(self,document_id:str,text:str)->str:
  if not document_id or len(document_id)>500: raise ValueError("invalid document id")
  if not isinstance(text,str): raise TypeError("text must be str")
  digest=hashlib.sha256(text.encode()).hexdigest(); old=self.db.execute("SELECT content_hash FROM documents WHERE id=?",(document_id,)).fetchone()
  if old and old[0]==digest: return "unchanged"
  step=self.chunk_chars-self.overlap; parts=[]; start=0
  while start<len(text):
   end=min(start+self.chunk_chars,len(text)); parts.append((start,end,text[start:end]))
   if end==len(text): break
   start+=step
  with self.db:
   self.db.execute("INSERT INTO documents VALUES(?,?) ON CONFLICT(id) DO UPDATE SET content_hash=excluded.content_hash",(document_id,digest))
   self.db.execute("DELETE FROM chunks WHERE document_id=?",(document_id,))
   for i,(a,b,chunk) in enumerate(parts):
    cid=hashlib.sha256(f"{document_id}:{digest}:{i}".encode()).hexdigest()
    self.db.execute("INSERT INTO chunks VALUES(?,?,?,?,?,?)",(cid,document_id,i,a,b,chunk))
  return "indexed"
 def delete(self,document_id):
  with self.db: cur=self.db.execute("DELETE FROM documents WHERE id=?",(document_id,))
  return cur.rowcount>0
 def get_chunks(self,document_id): return self.db.execute("SELECT ordinal,start_offset,end_offset,text FROM chunks WHERE document_id=? ORDER BY ordinal",(document_id,)).fetchall()
