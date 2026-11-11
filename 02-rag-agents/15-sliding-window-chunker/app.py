from dataclasses import dataclass
@dataclass(frozen=True)
class Window: index:int; start:int; end:int; text:str
def sliding_windows(text,window_chars=1000,overlap_chars=150):
 if window_chars<1 or overlap_chars<0 or overlap_chars>=window_chars: raise ValueError("invalid window/overlap")
 out=[]; step=window_chars-overlap_chars
 for start in range(0,len(text),step):
  end=min(start+window_chars,len(text)); out.append(Window(len(out)+1,start,end,text[start:end]))
  if end==len(text): break
 return out
