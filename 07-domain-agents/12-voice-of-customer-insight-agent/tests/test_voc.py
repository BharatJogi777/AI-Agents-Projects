from app.voc import summarize_voice_of_customer
import pytest

def test_aggregates_theme_counts_and_source_ids():
    result=summarize_voice_of_customer([{"source_id":"a","text":"App is slow"},{"source_id":"b","text":"Very slow loading"}])
    assert result.total_records==2 and result.theme_counts[0]==("performance",2) and result.source_ids==("a","b")

def test_rejects_empty_collection():
    with pytest.raises(ValueError): summarize_voice_of_customer([])
