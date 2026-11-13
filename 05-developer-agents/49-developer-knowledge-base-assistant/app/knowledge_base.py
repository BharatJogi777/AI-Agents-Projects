"""Local lexical knowledge search with explicit source attribution."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Article:
    title: str
    body: str
    source: str

def search_knowledge(query: str, articles: list[Article], *, limit: int = 5) -> list[dict]:
    if not isinstance(query,str) or not query.strip(): raise ValueError("query must not be empty")
    if not 1 <= limit <= 50: raise ValueError("limit must be between 1 and 50")
    terms = set(re.findall(r"[a-z0-9_]+", query.lower()))
    ranked=[]
    for article in articles:
        if not article.title.strip() or not article.source.strip(): raise ValueError("articles require title and source")
        title=set(re.findall(r"[a-z0-9_]+",article.title.lower()))
        body=set(re.findall(r"[a-z0-9_]+",article.body.lower()))
        score=3*len(terms & title)+len(terms & body)
        if score: ranked.append({"title":article.title,"source":article.source,"score":score,"excerpt":article.body[:400]})
    return sorted(ranked,key=lambda x:(-x["score"],x["title"]))[:limit]
