from dataclasses import dataclass
from pathlib import Path
@dataclass(frozen=True)
class IngestedDocument: source:str; text:str; metadata:dict
def ingest(path:str|Path,max_bytes:int=20000000)->list[IngestedDocument]:
 p=Path(path); ext=p.suffix.lower()
 if not p.is_file(): raise FileNotFoundError(p)
 if p.stat().st_size>max_bytes: raise ValueError("file too large")
 if ext in {".txt",".md"}: return [IngestedDocument(p.name,p.read_text(encoding="utf-8-sig"),{"format":ext[1:]})]
 if ext==".html":
  from html.parser import HTMLParser
  class Text(HTMLParser):
   def __init__(self): super().__init__(); self.skip=0; self.out=[]
   def handle_starttag(self,t,a):
    if t in {"script","style","noscript"}: self.skip+=1
   def handle_endtag(self,t):
    if t in {"script","style","noscript"} and self.skip: self.skip-=1
   def handle_data(self,d):
    if not self.skip and d.strip(): self.out.append(d.strip())
  q=Text(); q.feed(p.read_text(encoding="utf-8")); return [IngestedDocument(p.name,"\n".join(q.out),{"format":"html"})]
 if ext==".csv":
  import csv
  with p.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
  return [IngestedDocument(p.name,"\n".join(str(row) for row in rows),{"format":"csv","rows":len(rows)})]
 if ext==".json":
  import json
  data=json.loads(p.read_text(encoding="utf-8")); items=data if isinstance(data,list) else [data]
  return [IngestedDocument(p.name,json.dumps(v,ensure_ascii=False,sort_keys=True),{"format":"json","record":i}) for i,v in enumerate(items)]
 if ext==".pdf":
  from pypdf import PdfReader
  r=PdfReader(str(p)); return [IngestedDocument(p.name,page.extract_text() or "",{"format":"pdf","page":i}) for i,page in enumerate(r.pages,1)]
 if ext==".docx":
  from docx import Document
  d=Document(str(p)); return [IngestedDocument(p.name,x.text,{"format":"docx","paragraph":i}) for i,x in enumerate(d.paragraphs,1) if x.text.strip()]
 if ext==".xlsx":
  from openpyxl import load_workbook
  w=load_workbook(p,read_only=True,data_only=True); docs=[]
  try:
   for s in w.worksheets:
    for i,row in enumerate(s.iter_rows(values_only=True),1):
     if any(v is not None for v in row): docs.append(IngestedDocument(p.name," | ".join("" if v is None else str(v) for v in row),{"format":"xlsx","sheet":s.title,"row":i}))
  finally: w.close()
  return docs
 raise ValueError(f"unsupported file extension: {ext}")
