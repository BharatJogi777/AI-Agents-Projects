import pytest
from app.groundedness import score_groundedness

def test_all_sentences_overlap_evidence():
    r=score_groundedness("Python supports async tasks.",["Python supports async tasks and concurrency."])
    assert r.score == 1.0

def test_flags_unsupported_sentence():
    r=score_groundedness("Python supports async tasks. Mars has two moons.",["Python supports async tasks."])
    assert r.unsupported == ("Mars has two moons.",)

def test_threshold_validation():
    with pytest.raises(ValueError): score_groundedness("x",["x"],min_overlap=0)

def test_empty_answer_rejected():
    with pytest.raises(ValueError): score_groundedness(" ",["evidence"])
