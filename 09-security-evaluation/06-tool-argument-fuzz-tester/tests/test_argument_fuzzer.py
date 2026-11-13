from app.argument_fuzzer import generate_cases

def test_generates_type_edge_cases():
    cases = generate_cases(schema={"query":{"type":"string"},"limit":{"type":"integer"}})
    assert any(x["case"] == "null-byte" for x in cases)
    assert any(x["case"] == "huge-integer" for x in cases)

def test_rejects_unknown_type():
    import pytest
    with pytest.raises(ValueError): generate_cases(schema={"x":{"type":"object"}})
