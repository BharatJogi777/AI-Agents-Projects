from dataclasses import dataclass
@dataclass(frozen=True)
class Segment:
    start:float
    end:float
    text:str
    confidence:float
def assemble_transcript(segments:list[Segment])->dict:
    if not segments: raise ValueError("at least one segment is required")
    previous_end=0.0
    for s in segments:
        if s.start<0 or s.end<=s.start or s.start<previous_end: raise ValueError("segments must have valid, non-overlapping chronological timestamps")
        if not s.text.strip() or not 0<=s.confidence<=1: raise ValueError("text and confidence must be valid")
        previous_end=s.end
    return {"text":" ".join(s.text.strip() for s in segments),"segments":[s.__dict__ for s in segments],
            "low_confidence_segments":[i for i,s in enumerate(segments) if s.confidence<0.7],
            "requires_human_review":any(s.confidence<0.7 for s in segments)}
