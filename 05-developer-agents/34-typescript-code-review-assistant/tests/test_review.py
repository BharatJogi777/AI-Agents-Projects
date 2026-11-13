import pytest
from app.typescript_review import review
def test_detects_any_and_json_parse():
 r=review("let value: any = JSON.parse(raw)")
 assert len(r)==2
def test_line_number(): assert review("const x = 1;\n// @ts-ignore")[0]["line"]==2
def test_empty():
 with pytest.raises(ValueError): review("")
