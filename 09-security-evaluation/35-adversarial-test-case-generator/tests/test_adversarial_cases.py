import pytest
from app.adversarial_cases import generate_adversarial_cases

def test_generates_bounded_variants():
    r=generate_adversarial_cases("hello world")
    assert len(r)==5 and r[0].variant=="leading_space"

def test_limit_is_respected():
    assert len(generate_adversarial_cases("x",max_cases=2))==2

def test_zero_limit():
    assert generate_adversarial_cases("x",max_cases=0)==()

def test_invalid_limit_rejected():
    with pytest.raises(ValueError): generate_adversarial_cases("x",max_cases=6)
