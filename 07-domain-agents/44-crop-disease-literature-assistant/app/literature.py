from dataclasses import dataclass
@dataclass(frozen=True)
class Reference:
    reference_id: str
    title: str
    crop: str
    topic_terms: tuple[str,...]
    summary: str
    publication_year: int
    reviewed: bool
def search_literature(references: list[Reference], crop: str, question: str, current_year: int=2026) -> dict:
    if not crop.strip() or not question.strip(): raise ValueError("crop and question are required")
    seen=set(); tokens=set(question.lower().split()); matches=[]
    for r in references:
        if not r.reference_id.strip() or r.reference_id in seen: raise ValueError("reference ids must be non-empty and unique")
        if not r.title.strip() or not r.summary.strip(): raise ValueError("reference title and summary are required")
        if not 1900<=r.publication_year<=current_year: raise ValueError("publication year out of range")
        seen.add(r.reference_id)
        if r.crop.casefold()!=crop.casefold(): continue
        overlap=sorted(tokens & {t.lower() for t in r.topic_terms})
        if overlap: matches.append({"reference_id":r.reference_id,"title":r.title,"summary":r.summary,"publication_year":r.publication_year,"reviewed":r.reviewed,"matched_terms":overlap})
    matches.sort(key=lambda x:(not x["reviewed"],-x["publication_year"],x["reference_id"]))
    return {"crop":crop,"results":matches,"answer_status":"evidence_found" if matches else "insufficient_evidence","clinical_or_field_diagnosis_made":False,"consult_local_agronomist":True}
