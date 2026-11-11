from dataclasses import dataclass
import re
@dataclass(frozen=True)
class MarkdownChunk:
 index:int; heading_path:tuple[str,...]; start_line:int; end_line:int; text:str
def chunk_markdown(text:str,max_chars:int=1200)->list[MarkdownChunk]:
 if not isinstance(text,str): raise TypeError("text must be str")
 if max_chars<80: raise ValueError("max_chars must be at least 80")
 headings=[]; chunks=[]; buf=[]; start=1
 def flush(end):
  nonlocal buf,start
  content="\\n".join(buf).strip()
  if content: chunks.append(MarkdownChunk(len(chunks)+1,tuple(headings),start,end,content))
  buf=[]
 lines=text.splitlines()
 for no,line in enumerate(lines,1):
  m=re.match(r"^(#{1,6})\\s+(.+?)\\s*#*\\s*$",line)
  if m:
   flush(no-1); level=len(m.group(1)); headings[:]=headings[:level-1]; headings.append(m.group(2).strip()); start=no; buf=[line]; continue
  if not buf: start=no
  if buf and sum(len(x)+1 for x in buf)+len(line)+1>max_chars: flush(no-1); start=no
  buf.append(line)
 flush(len(lines)); return chunks
