from html.parser import HTMLParser
from dataclasses import dataclass
@dataclass(frozen=True)
class HTMLDocument: title:str; text:str; links:tuple[str,...]
class Parser(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.skip=[]; self.in_title=False; self.title=[]; self.parts=[]; self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs); hidden=tag in {"script","style","noscript","template","svg"} or "hidden" in a or a.get("aria-hidden")=="true" or "display:none" in a.get("style","").replace(" ","").lower()
  if hidden: self.skip.append(tag)
  if tag=="title": self.in_title=True
  if tag=="a" and a.get("href"): self.links.append(a["href"][:1000])
  if not self.skip and tag in {"p","div","br","li","h1","h2","h3","h4","h5","h6"}: self.parts.append("\\n")
 def handle_endtag(self,tag):
  if tag=="title": self.in_title=False
  if self.skip and self.skip[-1]==tag: self.skip.pop()
  if not self.skip and tag in {"p","div","br","li","h1","h2","h3","h4","h5","h6"}: self.parts.append("\\n")
 def handle_data(self,data):
  if self.skip: return
  if self.in_title: self.title.append(data.strip())
  elif data.strip(): self.parts.append(data.strip())
def extract_html(source:str,max_chars:int=200000)->HTMLDocument:
 if not isinstance(source,str): raise TypeError("source must be text")
 if len(source)>max_chars: raise ValueError("HTML input too large")
 p=Parser(); p.feed(source); p.close(); text="\\n".join(x.strip() for x in "".join(p.parts).splitlines() if x.strip())
 return HTMLDocument(" ".join(p.title),text,tuple(dict.fromkeys(p.links)))
