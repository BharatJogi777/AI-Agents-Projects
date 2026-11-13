"""Route explicit speech transcripts to a fixed, non-executing intent catalogue."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Intent:
    name:str
    phrases:tuple[str,...]
    requires_confirmation:bool=True
def route_command(transcript:str,intents:list[Intent])->dict:
    text=transcript.strip().casefold()
    if not text: raise ValueError("transcript cannot be empty")
    matches=[]
    for intent in intents:
        if not intent.name.strip() or not intent.phrases: raise ValueError("intent definitions need a name and phrases")
        if any(text==phrase.strip().casefold() for phrase in intent.phrases): matches.append(intent)
    if len(matches)>1: return {"status":"ambiguous","candidates":[i.name for i in matches],"execute":False}
    if not matches: return {"status":"unmatched","execute":False}
    i=matches[0]
    return {"status":"matched","intent":i.name,"requires_confirmation":i.requires_confirmation,"execute":False}
