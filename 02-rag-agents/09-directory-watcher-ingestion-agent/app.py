from dataclasses import dataclass
from pathlib import Path
import hashlib
@dataclass(frozen=True)
class Change: kind:str; path:str; sha256:str|None
class DirectoryWatcher:
 def __init__(self,root:str|Path,extensions=(".txt",".md",".pdf",".docx"),max_file_bytes=20000000):
  self.root=Path(root).resolve(); self.extensions={x.lower() for x in extensions}; self.max_file_bytes=max_file_bytes; self.snapshot={}
  if not self.root.is_dir(): raise ValueError("root must be an existing directory")
 def scan(self):
  current={}
  for p in self.root.rglob("*"):
   if p.is_symlink() or not p.is_file() or p.suffix.lower() not in self.extensions: continue
   try:
    p.resolve(strict=True).relative_to(self.root)
    if p.stat().st_size>self.max_file_bytes: continue
    current[str(p.relative_to(self.root))]=hashlib.sha256(p.read_bytes()).hexdigest()
   except (OSError,ValueError): continue
  changes=[]
  for name,digest in sorted(current.items()):
   old=self.snapshot.get(name); kind="created" if old is None else "modified" if old!=digest else None
   if kind: changes.append(Change(kind,name,digest))
  for name in sorted(self.snapshot.keys()-current.keys()): changes.append(Change("deleted",name,None))
  self.snapshot=current; return changes
