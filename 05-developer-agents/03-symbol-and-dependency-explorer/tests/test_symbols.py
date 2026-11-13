import pytest
from app.symbols import extract_symbols, import_dependencies

def test_nested_symbols_and_imports():
    src="import os\nclass Service:\n def run(self): pass\nasync def fetch(): pass\n"
    symbols=extract_symbols(src)
    assert [(s.name,s.kind,s.parent) for s in symbols] == [("Service","class",None),("run","function","Service"),("fetch","async_function",None)]
    assert import_dependencies(src) == ("os",)

def test_invalid_syntax():
    with pytest.raises(ValueError): extract_symbols("class :")
