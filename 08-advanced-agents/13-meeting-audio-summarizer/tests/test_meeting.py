import pytest
from app.meeting import Utterance,summarize_transcript
def test_builds_traceable_summary_input():
 r=summarize_transcript([Utterance("A",0,2,"We should ship."),Utterance("B",2,4,"I agree.")])
 assert r["speakers"]==["A","B"] and not r["decisions_verified"]
def test_rejects_overlapping_utterances():
 with pytest.raises(ValueError): summarize_transcript([Utterance("A",0,3,"one"),Utterance("B",2,4,"two")])
def test_rejects_empty_transcript():
 with pytest.raises(ValueError): summarize_transcript([])
