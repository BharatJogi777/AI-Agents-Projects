from app.feedback import analyze_feedback
import pytest

def test_detects_themes_and_negative_sentiment():
    result=analyze_feedback("The app is slow and confusing")
    assert "performance" in result.themes and "usability" in result.themes and result.sentiment=="negative"

def test_rejects_empty_feedback():
    with pytest.raises(ValueError): analyze_feedback(" ")
