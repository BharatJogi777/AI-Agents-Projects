import pytest
from app.doc_generator import generate
def test_public_only():
 out=generate('def hello():\n """Say hello."""\n pass\n\ndef _private(): pass','sample'); assert "hello" in out and "Say hello." in out and "_private" not in out
def test_syntax_error():
 with pytest.raises(ValueError): generate("def (")
