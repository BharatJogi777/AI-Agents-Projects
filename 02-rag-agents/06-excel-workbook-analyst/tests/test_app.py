from io import BytesIO
import pytest
from openpyxl import Workbook
from app import extract_workbook
def test_sheet_row_provenance():
 w=Workbook(); s=w.active; s.title="Sales"; s.append(["item","qty"]); s.append(["tea",3]); b=BytesIO(); w.save(b)
 rows=extract_workbook(b.getvalue()); assert rows[1].sheet=="Sales" and rows[1].row_number==2 and rows[1].values==("tea",3)
def test_size_and_row_limits():
 w=Workbook(); w.active.append(["a"]); w.active.append(["b"]); b=BytesIO(); w.save(b)
 with pytest.raises(ValueError): extract_workbook(b.getvalue(),max_bytes=10)
 with pytest.raises(ValueError): extract_workbook(b.getvalue(),max_rows=1)
