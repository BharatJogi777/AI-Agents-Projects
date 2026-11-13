import re
def answer(question: str, documents: list[dict], min_score: int = 1) -> dict:
    if not question.strip(): raise ValueError("question is required")
    if min_score<1: raise ValueError("min_score must be positive")
    terms=set(re.findall(r"[a-z0-9]+",question.lower())); hits=[]
    for doc in documents:
        if not doc.get("id") or not doc.get("text"): raise ValueError("each document needs id and text")
        score=len(terms & set(re.findall(r"[a-z0-9]+",doc["text"].lower())))
        if score>=min_score: hits.append({"document_id":str(doc["id"]),"text":doc["text"],"score":score})
    hits.sort(key=lambda x:(-x["score"],x["document_id"]))
    return {"status":"answered_with_sources" if hits else "abstain","matches":hits[:5],"human_resources_contact_recommended":not bool(hits),"employment_decision":False}
