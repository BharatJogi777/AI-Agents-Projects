import math,re
from .contracts import Memory,RankedMemory
def _terms(text):return set(re.findall(r"[^\\W_]+",text.casefold(),flags=re.UNICODE))
def retrieve_ranked(query,memories,now,limit=5,min_confidence=.5):
    if not isinstance(query,str) or not query.strip() or type(limit) is not int or limit<1:raise ValueError("query and positive limit required")
    if isinstance(now,bool) or not isinstance(now,(int,float)) or not math.isfinite(now):raise ValueError("now must be finite")
    if isinstance(min_confidence,bool) or not isinstance(min_confidence,(int,float)) or not math.isfinite(min_confidence) or not 0<=min_confidence<=1:raise ValueError("min_confidence must be 0..1")
    terms=_terms(query);ranked=[];seen=set()
    for m in memories:
        if not isinstance(m,Memory) or m.id in seen:continue
        seen.add(m.id)
        if not m.confirmed or m.sensitive or not isinstance(m.text,str) or not m.text.strip():continue
        if isinstance(m.confidence,bool) or not isinstance(m.confidence,(int,float)) or not math.isfinite(m.confidence) or not 0<=m.confidence<=1 or m.confidence<min_confidence:continue
        if isinstance(m.created_at,bool) or not isinstance(m.created_at,(int,float)) or not math.isfinite(m.created_at):continue
        if m.expires_at is not None and (isinstance(m.expires_at,bool) or not isinstance(m.expires_at,(int,float)) or not math.isfinite(m.expires_at) or m.expires_at<=now):continue
        overlap=len(terms&_terms(m.text))/max(1,len(terms))
        if overlap:
            recency=1/(1+max(0,now-m.created_at)/86400)
            score=.65*overlap+.25*m.confidence+.1*recency
            ranked.append(RankedMemory(m,score))
    ranked.sort(key=lambda x:(-x.score,-x.memory.created_at,x.memory.id))
    return ranked[:limit]
def retrieve(query,memories,now,limit=5,min_confidence=.5):
    return [item.memory for item in retrieve_ranked(query,memories,now,limit,min_confidence)]
