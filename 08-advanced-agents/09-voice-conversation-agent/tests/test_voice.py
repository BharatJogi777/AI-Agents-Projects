import pytest
from app.voice import VoiceTurn,append_turn
def test_alternating_turns():
 h=append_turn([],VoiceTurn("user","Hi",1)); h=append_turn(h,VoiceTurn("assistant","Hello",2))
 assert len(h)==2
def test_rejects_duplicate_speaker():
 with pytest.raises(ValueError): append_turn([VoiceTurn("user","Hi",1)],VoiceTurn("user","Again",2))
def test_rejects_sequence_gap():
 with pytest.raises(ValueError): append_turn([],VoiceTurn("user","Hi",2))
