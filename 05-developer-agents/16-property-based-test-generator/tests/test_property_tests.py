import pytest
from app.property_tests import generate_properties, render_pytest, to_json


def test_generates_one_spec_per_invariant():
    props = generate_properties("normalize", {"value": "string"}, ["idempotent", "stable"])
    assert len(props) == 2
    assert "idempotent" in props[0].invariant
    assert "NotImplementedError" in render_pytest("normalize", props)
    assert '"example_strategy"' in to_json(props)


def test_rejects_missing_invariants_and_invalid_names():
    with pytest.raises(ValueError):
        generate_properties("normalize", {}, [])
    with pytest.raises(ValueError):
        generate_properties("not-valid", {}, ["stable"])


def test_rejects_invalid_domain():
    with pytest.raises(ValueError):
        generate_properties("f", {"bad-name": "text"}, ["invariant"])
