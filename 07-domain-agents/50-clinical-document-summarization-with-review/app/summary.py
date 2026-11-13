from dataclasses import dataclass
@dataclass(frozen=True)
class ClinicalNote:
    document_id: str
    patient_reference: str
    author_reference: str
    document_date: str
    sections: dict[str,str]
    source_refs: tuple[str,...]
def prepare_review_packet(note: ClinicalNote) -> dict:
    if not all(x.strip() for x in (note.document_id,note.patient_reference,note.author_reference,note.document_date)): raise ValueError("document, patient, author and date references are required")
    if not note.sections or any(not k.strip() or not isinstance(v,str) or not v.strip() for k,v in note.sections.items()): raise ValueError("clinical sections must have non-empty names and text")
    if not note.source_refs or any(not x.strip() for x in note.source_refs): raise ValueError("source references are required")
    return {"document_id":note.document_id,"patient_reference":note.patient_reference,"author_reference":note.author_reference,"document_date":note.document_date,"section_inventory":[{"section":k,"character_count":len(v)} for k,v in note.sections.items()],"source_refs":list(note.source_refs),"summary_text_generated":False,"clinical_interpretation_performed":False,"clinician_review_required":True,"patient_facing_output_authorized":False}
