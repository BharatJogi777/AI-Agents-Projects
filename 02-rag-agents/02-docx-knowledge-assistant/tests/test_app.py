from io import BytesIO
from docx import Document
from app import extract_docx
def test_paragraph_and_table_order():
 d=Document(); d.add_paragraph("Intro"); t=d.add_table(rows=1,cols=2); t.cell(0,0).text="Name"; t.cell(0,1).text="Value"; d.add_paragraph("End")
 b=BytesIO(); d.save(b); rows=extract_docx(b.getvalue())
 assert [x.kind for x in rows]==["paragraph","table_row","paragraph"] and rows[1].text=="Name | Value"
def test_empty_document():
 d=Document(); b=BytesIO(); d.save(b); assert extract_docx(b.getvalue())==[]
