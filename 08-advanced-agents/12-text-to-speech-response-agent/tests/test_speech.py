import pytest
from app.speech import SpeechRequest,prepare_speech
def test_prepares_allowlisted_request():
 r=prepare_speech(SpeechRequest("Hello","en-US","voice-a"),{"voice-a"},{"en-US"})
 assert r["text"]=="Hello" and not r["synthesis_requested"]
def test_rejects_unknown_voice():
 with pytest.raises(ValueError): prepare_speech(SpeechRequest("Hi","en-US","other"),{"voice-a"},{"en-US"})
def test_rejects_oversized_text():
 with pytest.raises(ValueError): prepare_speech(SpeechRequest("12345","en","v"),{"v"},{"en"},4)
