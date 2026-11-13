def discover(query: str, catalog: list[dict], limit: int = 5) -> dict:
    if not query.strip(): raise ValueError("query is required")
    if not 1<=limit<=50: raise ValueError("limit must be between 1 and 50")
    terms=set(query.casefold().split()); matches=[]
    for p in catalog:
        if not p.get("id") or not p.get("name"): raise ValueError("catalog items require id and name")
        searchable=" ".join([p["name"],p.get("description","")," ".join(p.get("tags",[]))]).casefold()
        score=sum(term in searchable for term in terms)
        if score: matches.append({"product_id":p["id"],"name":p["name"],"description":p.get("description",""),"match_score":score,"price":p.get("price"),"availability":p.get("availability","unknown")})
    matches.sort(key=lambda x:(-x["match_score"],x["name"].casefold(),x["product_id"]))
    return {"query":query.strip(),"results":matches[:limit],"ranking_basis":"query term matches only","purchase_performed":False}
