import pytest
from app.survey_analysis import analyze_survey

def test_reports_distribution_and_missing_responses():
    result=analyze_survey(responses=[{"Satisfaction":"High"},{"Satisfaction":"High"},{"Satisfaction":""},{}],questions=["Satisfaction"])
    assert result[0].response_count==2
    assert result[0].missing_count==2
    assert result[0].distribution=={"High":2}

def test_empty_survey_has_all_missing():
    result=analyze_survey(responses=[{}],questions=["NPS"])
    assert result[0].missing_count==1
    assert result[0].distribution=={}

def test_rejects_duplicate_questions():
    with pytest.raises(ValueError,match="unique"):
        analyze_survey(responses=[],questions=["A","A"])
