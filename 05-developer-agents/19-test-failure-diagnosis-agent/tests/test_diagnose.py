import pytest
from app.diagnose import diagnose_output, to_json


def test_classifies_assertion_and_import_failures():
    results = diagnose_output("tests/test_api.py:12: AssertionError: mismatch\ntests/test_db.py:8: ModuleNotFoundError: psycopg")
    assert [x.kind for x in results] == ["assertion", "import"]
    assert "expected" in to_json(results)


def test_unrecognized_nonempty_output_is_preserved():
    result = diagnose_output("collection interrupted")[0]
    assert result.kind == "unclassified"
    assert "collection interrupted" in result.evidence


def test_type_validation():
    with pytest.raises(TypeError):
        diagnose_output(None)
