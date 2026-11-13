import pytest
from app.screenshot import ScreenshotObservation,explain_ui
def test_explanation_preserves_uncertainty():
 o=ScreenshotObservation("shot-1","settings page",("Save button","Email field"),("field value unreadable",))
 r=explain_ui(o)
 assert r["uncertainties"]==["field value unreadable"]
 assert r["recommendations_require_human_review"]
def test_requires_observed_elements():
 with pytest.raises(ValueError): explain_ui(ScreenshotObservation("x","page",()))
