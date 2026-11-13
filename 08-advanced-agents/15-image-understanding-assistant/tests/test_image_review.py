import pytest
from app.image_review import ImageObservation,describe_observation
def test_preserves_observations_and_uncertainty():
 r=describe_observation(ImageObservation("upload-1",("red car",),("STOP",),("plate unreadable",)))
 assert r["visible_text"]==["STOP"] and r["uncertain_details"]==["plate unreadable"]
def test_requires_image_reference():
 with pytest.raises(ValueError): describe_observation(ImageObservation(" ",("object",)))
def test_rejects_blank_observation():
 with pytest.raises(ValueError): describe_observation(ImageObservation("img",("",)))
