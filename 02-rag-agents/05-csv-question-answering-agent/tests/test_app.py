import pytest
from app import parse_csv
def test_quoted_fields_and_lines():
 r=parse_csv('name,notes\\nAda,"works, remotely"\\nLin,"line 1\\nline 2"')
 assert r[0].row_number==2 and r[0].values["notes"]=="works, remotely" and r[1].values["notes"]=="line 1\\nline 2"
def test_header_and_limits():
 with pytest.raises(ValueError): parse_csv("a,a\\n1,2")
 with pytest.raises(ValueError): parse_csv("a\\n123",max_bytes=2)
 with pytest.raises(ValueError): parse_csv("a\\n1\\n2",max_rows=1)
