"""Build chapter boundaries and transcript inputs; no video decoding is performed."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Chapter:
    start:float
    end:float
    title:str
    transcript:str
def build_chapters(duration:float,chapters:list[Chapter])->dict:
    if duration<=0 or not chapters: raise ValueError("positive video duration and chapters are required")
    previous=0.0
    for c in chapters:
        if c.start<previous or c.end<=c.start or c.end>duration: raise ValueError("chapters must be ordered, non-overlapping, and within video duration")
        if not c.title.strip() or not c.transcript.strip(): raise ValueError("chapter title and transcript are required")
        previous=c.end
    return {"duration_seconds":duration,"chapters":[c.__dict__ for c in chapters],"summary_inputs":[{"title":c.title,"transcript":c.transcript} for c in chapters],"summary_generated":False}
