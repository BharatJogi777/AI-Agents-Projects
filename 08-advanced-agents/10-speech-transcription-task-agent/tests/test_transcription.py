import pytest
from app.transcription import Segment,assemble_transcript
def test_assembles_segments():
 r=assemble_transcript([Segment(0,1,"Hello",.99),Segment(1,2,"world",.95)])
 assert r["text"]=="Hello world" and not r["requires_human_review"]
def test_flags_low_confidence():
 assert assemble_transcript([Segment(0,1,"maybe",.4)])["requires_human_review"]
def test_rejects_overlapping_segments():
 with pytest.raises(ValueError): assemble_transcript([Segment(0,2,"a",.9),Segment(1,3,"b",.9)])
