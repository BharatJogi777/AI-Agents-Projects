from dataclasses import dataclass
import re
@dataclass(frozen=True)
class SemanticChunk: index:int; start:int; end:int; text:str
def semantic_chunks(text,similarity,threshold=.55,min_chars=100,max_chars=1200):
 if not 0<=threshold<=1 or min_chars<1 or max_chars<min_chars: raise ValueError("invalid chunk configuration")
 sentences=[(m.start(),m.end(),m.group().strip()) for m in re.finditer(r"\S.*?(?:[.!?](?=\s|$)|$)",text,re.S)]
 chunks=[]; start=0; end=0; parts=[]
 for a,b,s in sentences:
  split=bool(parts) and (len(" ".join(parts+[s]))>max_chars or (len(" ".join(parts))>=min_chars and similarity(" ".join(parts),s)<threshold))
  if split: chunks.append(SemanticChunk(len(chunks)+1,start,end," ".join(parts))); start=a; parts=[s]
  else: parts.append(s)
  end=b
 if parts: chunks.append(SemanticChunk(len(chunks)+1,start,end," ".join(parts)))
 return chunks
