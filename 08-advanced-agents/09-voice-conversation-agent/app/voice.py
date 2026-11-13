from dataclasses import dataclass
@dataclass(frozen=True)
class VoiceTurn:
    speaker:str
    transcript:str
    sequence:int
    interrupted:bool=False
def validate_turn(turn:VoiceTurn,expected_sequence:int)->VoiceTurn:
    if turn.speaker not in {"user","assistant"}: raise ValueError("speaker must be user or assistant")
    if turn.sequence!=expected_sequence: raise ValueError("unexpected turn sequence")
    if not turn.transcript.strip(): raise ValueError("transcript cannot be empty")
    return turn
def append_turn(history:list[VoiceTurn],turn:VoiceTurn)->list[VoiceTurn]:
    validate_turn(turn,len(history)+1)
    if history and history[-1].speaker==turn.speaker: raise ValueError("conversation speakers must alternate")
    if turn.interrupted and turn.speaker!="user": raise ValueError("only a user interruption is supported")
    return [*history,turn]
