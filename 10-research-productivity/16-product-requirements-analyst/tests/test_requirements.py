import pytest
from app.requirements import analyze_requirements

def test_normalizes_and_preserves_source_traceability():
    result = analyze_requirements(needs=[{"statement":" Export data ","source":"Interview 4","priority":"HIGH","acceptance_criteria":[" CSV download "]}])
    assert result[0].requirement_id == "REQ-001"
    assert result[0].statement == "Export data"
    assert result[0].source == "Interview 4"
    assert result[0].acceptance_criteria == ("CSV download",)

def test_rejects_missing_source():
    with pytest.raises(ValueError, match="source"):
        analyze_requirements(needs=[{"statement":"Export data"}])

def test_rejects_duplicate_ids():
    item={"id":"R1","statement":"A","source":"Call"}
    with pytest.raises(ValueError, match="duplicate"):
        analyze_requirements(needs=[item,item])
