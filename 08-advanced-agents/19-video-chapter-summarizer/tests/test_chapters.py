import pytest
from app.chapters import Chapter,build_chapters
def test_builds_chapter_inputs():
 r=build_chapters(100,[Chapter(0,40,"Intro","Welcome"),Chapter(40,90,"Main","Details")])
 assert len(r["summary_inputs"])==2 and not r["summary_generated"]
def test_rejects_overlap():
 with pytest.raises(ValueError): build_chapters(100,[Chapter(0,60,"A","x"),Chapter(50,90,"B","y")])
def test_rejects_chapter_beyond_duration():
 with pytest.raises(ValueError): build_chapters(10,[Chapter(0,11,"A","x")])
