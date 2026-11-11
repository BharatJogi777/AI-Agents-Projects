import pytest
from app import IntentClassifier
def test_valid_high_confidence_result():
    c=IntentClassifier({"billing","support"},lambda _:{"intent":"billing","confidence":.93})
    assert c.classify("invoice").needs_human_review is False
def test_low_confidence_requires_review():
    c=IntentClassifier({"billing"},lambda _:{"intent":"billing","confidence":.4},.7)
    assert c.classify("unclear").needs_human_review
def test_invalid_intent_or_confidence_rejected():
    with pytest.raises(ValueError): IntentClassifier({"billing"},lambda _:{"intent":"admin","confidence":.9}).classify("x")
    with pytest.raises(ValueError): IntentClassifier({"billing"},lambda _:{"intent":"billing","confidence":True}).classify("x")
def test_empty_input_and_invalid_payload():
    with pytest.raises(ValueError): IntentClassifier({"billing"},lambda _:{}).classify(" ")
    with pytest.raises(ValueError): IntentClassifier({"billing"},lambda _:[]).classify("x")
