"""Build a traceable meeting summary draft from timestamped transcript segments."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Utterance:
    speaker:str
    start:float
    end:float
    text:str
def summarize_transcript(utterances:list[Utterance])->dict:
    if not utterances: raise ValueError("transcript must contain utterances")
    previous=0.0
    speakers=set()
    for u in utterances:
        if not u.speaker.strip() or not u.text.strip() or u.start<0 or u.end<=u.start or u.start<previous: raise ValueError("utterances require speaker, text, and ordered valid timestamps")
        previous=u.end; speakers.add(u.speaker)
    return {"summary_input":"\n".join(f"{u.speaker}: {u.text.strip()}" for u in utterances),
            "speakers":sorted(speakers),"duration_seconds":utterances[-1].end,
            "summary_status":"draft_input_only","decisions_verified":False,"action_items_verified":False}
