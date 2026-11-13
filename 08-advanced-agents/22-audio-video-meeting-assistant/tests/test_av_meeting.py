import pytest
from app.av_meeting import Marker, build_timeline

def test_sorts_and_reports_cross_media_overlap():
    result = build_timeline([Marker("v","video",100,300,"frame"), Marker("t","transcript",150,200,"hello")])
    assert [m.marker_id for m in result.markers] == ["v","t"]
    assert result.overlaps == (("v","t"),)
    assert result.duration_ms == 300

def test_rejects_invalid_ranges_and_duplicate_ids():
    with pytest.raises(ValueError): build_timeline([Marker("x","audio",4,4,"x")])
    m = Marker("x","audio",0,10,"x")
    with pytest.raises(ValueError): build_timeline([m,m])

def test_rejects_empty_content_and_invalid_media():
    with pytest.raises(ValueError): build_timeline([Marker("x","audio",0,1," ")])
    with pytest.raises(ValueError): build_timeline([Marker("x","image",0,1,"x")])
