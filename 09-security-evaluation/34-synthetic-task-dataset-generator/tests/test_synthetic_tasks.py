import pytest
from app.synthetic_tasks import generate_tasks

T=[{"prompt":"Summarize order {id}","expected":"summary"},{"prompt":"Classify ticket {id}","expected":"category"}]

def test_reproducible_seed():
    assert generate_tasks(T,count=10,seed=42) == generate_tasks(T,count=10,seed=42)

def test_count_and_ids():
    r=generate_tasks(T,count=3)
    assert len(r)==3 and r[0].case_id=="synthetic-00001"

def test_zero_count():
    assert generate_tasks(T,count=0) == ()

def test_invalid_template_rejected():
    with pytest.raises(ValueError): generate_tasks([{"prompt":"x"}],count=1)
