"""Prepare safe, bounded text payloads for a separate speech synthesis adapter."""
from dataclasses import dataclass
@dataclass(frozen=True)
class SpeechRequest:
    text:str
    language:str
    voice_id:str
def prepare_speech(req:SpeechRequest,allowed_voices:set[str],allowed_languages:set[str],max_chars:int=2000)->dict:
    if not req.text.strip(): raise ValueError("speech text cannot be empty")
    if len(req.text)>max_chars or max_chars<1: raise ValueError("speech text exceeds configured length")
    if req.voice_id not in allowed_voices or req.language not in allowed_languages: raise ValueError("voice or language is not allowlisted")
    return {"text":req.text.strip(),"language":req.language,"voice_id":req.voice_id,"synthesis_requested":False}
