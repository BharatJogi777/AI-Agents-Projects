import re
def rewrite_query(query,rewriter,max_variants=3,max_chars=500):
 if not query or len(query)>max_chars: raise ValueError("query empty or too long")
 if not 0<=max_variants<=5: raise ValueError("max_variants must be 0..5")
 raw=rewriter(query)
 if not isinstance(raw,list): raise TypeError("rewriter must return a list")
 out=[query]; seen={query.casefold()}
 for item in raw:
  if not isinstance(item,str): continue
  v=re.sub(r"\\s+"," ",item).strip()
  if v and len(v)<=max_chars and v.casefold() not in seen: out.append(v); seen.add(v.casefold())
  if len(out)>=max_variants+1: break
 return out
